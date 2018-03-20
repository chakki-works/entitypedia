# -*- coding: utf-8 -*-
"""
Preprocessors.
"""
import itertools
import re

import MeCab
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.externals import joblib
from gensim.corpora.dictionary import Dictionary
t = MeCab.Tagger('-Owakati')

UNK = '<UNK>'
PAD = '<PAD>'
unk_vec = np.zeros(shape=(50,))


def normalize_number(text):
    return re.sub(r'[0-9０１２３４５６７８９]', r'0', text)


class Preprocessor(BaseEstimator, TransformerMixin):

    def __init__(self, window_size=3, word_embeddings=None):
        self._window_size = window_size
        self._word_embeddings = word_embeddings
        self.word_dic = Dictionary()
        self.label_dic = Dictionary()

    def fit(self, X, y=None):
        self.word_dic.add_documents(X)
        self.label_dic.add_documents(y)

        return self

    def transform(self, X, y=None):
        inputs = []
        outputs = list(itertools.chain(*y))
        for sent in X:
            padded_sent = self.padding(sent)
            for i in range(self._window_size, len(sent) + self._window_size):
                window_words = padded_sent[i - self._window_size: i + self._window_size + 1]
                embedding = self.to_embedding(window_words)
                assert embedding.shape == ((self._window_size * 2 + 1) * 50,)
                inputs.append(embedding)

        assert len(inputs) == len(outputs)

        return (inputs, outputs) if outputs is not None else inputs

    def padding(self, sent):
        return [PAD] * self._window_size + sent + [PAD] * self._window_size

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


def batch_iter(data, labels, batch_size=32, shuffle=True, preprocess=None):
    num_batches_per_epoch = int((len(data) - 1) / batch_size) + 1

    def data_generator():
        """
        Generates a batch iterator for a dataset.
        """
        data_size = len(data)
        while True:
            indices = np.arange(data_size)
            # Shuffle the data at each epoch
            if shuffle:
                indices = np.random.permutation(indices)

            for batch_num in range(num_batches_per_epoch):
                start_index = batch_num * batch_size
                end_index = min((batch_num + 1) * batch_size, data_size)
                # X = [d[indices[start_index: end_index]] for d in data]
                X = [data[i] for i in indices[start_index: end_index]]
                y = [labels[i] for i in indices[start_index: end_index]]
                yield preprocess(X, y)

    return num_batches_per_epoch, data_generator()


def tokenize(text):
    """Tokenize Japanese text.

    Args:
        text: Japanese string.

    Returns:
        A list of words.
    """
    words = t.parse(text).rstrip().split()

    return words
