# -*- coding: utf-8 -*-
"""
Preprocessors.
"""
import itertools
import re

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.externals import joblib

UNK = '<UNK>'
PAD = '<PAD>'
unk_vec = np.zeros(shape=(50,))


def normalize_number(text):
    return re.sub(r'[0-9０１２３４５６７８９]', r'0', text)


class Preprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, window_size=3, word_embeddings=None, vocab_init=None):
        self._window_size = window_size
        self._word_embeddings = word_embeddings
        self._vocab_init = vocab_init or {}
        self.word_dic = {PAD: 0, UNK: 1}
        self.char_dic = {PAD: 0, UNK: 1}
        self.label_dic = {PAD: 0}

    def fit(self, X, y=None):
        for w in set(itertools.chain(*X)) | set(self._vocab_init):
            self.word_dic[w] = len(self.word_dic)

        # create label dictionary
        for t in set(itertools.chain(*y)):
            self.label_dic[t] = len(self.label_dic)

        return self

    def transform(self, X, y=None):
        inputs = []
        outputs = []
        for sent in X:
            padded_sent = self.padding(sent)
            for i in range(self._window_size, len(sent) + self._window_size):
                window_words = padded_sent[i - self._window_size: i + self._window_size]
                embedding = self.to_embedding(window_words)
                inputs.append(embedding)

        if y is not None:
            for labels in y:
                padded_labels = self.padding(labels)
            y = np.array([[self.label_dic[t] for t in sent] for sent in y])

        return (inputs, outputs) if outputs is not None else inputs

    def padding(self, sent):
        return [UNK] * self._window_size + sent + [UNK] * self._window_size

    def to_embedding(self, sent):
        embs = [self._word_embeddings[w]
                if w in self._word_embeddings else
                unk_vec for w in sent]
        return np.concatenate(embs)

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y).transform(X, y)

    def inverse_transform(self, docs):
        id2label = {i: t for t, i in self.label_dic.items()}

        return [[id2label[t] for t in doc] for doc in docs]

    def save(self, file_path):
        joblib.dump(self, file_path)

    @classmethod
    def load(cls, file_path):
        p = joblib.load(file_path)

        return p
