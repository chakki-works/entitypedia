import os
import json

import MeCab
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report
t = MeCab.Tagger('-Owakati')


def tokenize(text):
    words = t.parse(text).rstrip().split()

    return words


def input_fn(file_path, word_indices, label_indices, maxlen=50):
    jsons = load_jsonl(file_path)

    X, y = [], []
    for j in jsons:
        words = tokenize(j['text'])
        X.append(words)
        y.append(j['label'])

    X = word2id(X, word_indices)
    y = label2id(y, label_indices)
    X = pad_sequences(X, maxlen=maxlen)

    return X, y


def evaluate_f1(y_true, y_pred, label_indices):
    id2label = {v: k for k, v in label_indices.items()}
    target_names = [id2label[id] for id in sorted(id2label)]
    print(classification_report(y_true, y_pred, target_names=target_names))


def load_jsonl(file):
    with open(file) as f:
        for line in f:
            j = json.loads(line)
            yield j


def maybe_create_indices(file_path, save_path):
    if os.path.exists(save_path):
        with open(save_path) as f:
            word_indices, label_indices = json.load(f)
        return word_indices, label_indices
    X, y = [], []
    for j in load_jsonl(file_path):
        X.append(tokenize(j['text']))
        y.append(j['label'])
    word_indices, label_indices = create_indices(X, y)

    with open(save_path, 'w') as f:
        f.write(json.dumps([word_indices, label_indices]))

    return word_indices, label_indices


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
