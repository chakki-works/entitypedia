import json
import os

import MeCab
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from sklearn.model_selection import train_test_split


t = MeCab.Tagger('-Owakati')


def load_jsonl(file):
    with open(file) as f:
        for line in f:
            j = json.loads(line)
            yield j


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


if __name__ == '__main__':
    print('Loading data...')
    BASE = os.path.join(os.path.dirname(__file__), '../../data/')
    file_seed = os.path.join(BASE, 'seeds.jsonl')
    file_abstract = os.path.join(BASE, 'abstracts.jsonl')

    seeds = dict([(j['id'], j['class']) for j in load_jsonl(file_seed)])
    abstracts = load_jsonl(file_abstract)

    X, y = [], []
    for abstract in abstracts:
        id = abstract['id']
        if id not in seeds:
            continue
        text = abstract['text']
        text = t.parse(text).strip().split()
        label = seeds[id]
        X.append(text)
        y.append(label)
    print('#X: {}'.format(len(X)))

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
              epochs=1,
              validation_data=(x_test, y_test))
    score, acc = model.evaluate(x_test, y_test,
                                batch_size=batch_size)
    print('Test score:', score)
    print('Test accuracy:', acc)
