from __future__ import print_function
import csv
import glob
import json
import os
from collections import defaultdict

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.datasets import imdb
import MeCab
from sklearn.model_selection import train_test_split

t = MeCab.Tagger('-Owakati')


def load_seeds(dir):
    files = glob.glob(os.path.join(dir, '*.csv'))
    ne_dic = defaultdict(list)
    for file in files:
        category = file.split('/')[-1].split('.csv')[0]
        with open(file) as f:
            reader = csv.reader(f)
            for raw in reader:
                instance = raw[0]
                ne_dic[category].append(instance)

    return ne_dic


def load_data(file_path, ne_dic):
    X, y = [], []
    with open(file_path) as f:
        docs = json.load(f)
    for category, instances in ne_dic.items():
        for ins in instances:
            if ins not in docs:
                continue
            text = docs[ins]
            text = t.parse(text).strip().split()
            X.append(text)
            y.append(category)

    return X, y


def create_indices(X, y):
    word_indices = {'PAD': 0, 'UNK': 1}
    label_indices = {}
    for sent in X:
        for w in sent:
            if w in word_indices:
                continue
            word_indices[w] = len(word_indices)
    for cat in y:
        if cat in label_indices:
            continue
        label_indices[cat] = len(label_indices)

    return word_indices, label_indices


def word2id(X, word_indices):
    docs = []
    for sent in X:
        doc = [word_indices[w] for w in sent]
        docs.append(doc)

    return docs


def label2id(y, label_indices):
    return [label_indices[l] for l in y]


print('Loading data...')
seeds_dir = os.path.join(os.path.dirname(__file__), '../data/seeds')
ne_dic = load_seeds(seeds_dir)
file_path = './docs.json'
print(ne_dic)
X, y = load_data(file_path, ne_dic)
print(X[0])
word_indices, label_indices = create_indices(X, y)
print(word_indices)
X = word2id(X, word_indices)
y = label2id(y, label_indices)
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')


max_features = len(word_indices)
maxlen = 100  # cut texts after this number of words (among top max_features most common words)
batch_size = 32


print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)

print('Build model...')
model = Sequential()
model.add(Embedding(max_features, 128, mask_zero=True))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(len(label_indices), activation='softmax'))

# try using different optimizers and different optimizer configs
model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

print('Train...')
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=15,
          validation_data=(x_test, y_test))
score, acc = model.evaluate(x_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)
