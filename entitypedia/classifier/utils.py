"""
Utilities for manipulating the loss collections.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import MeCab
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing.sequence import pad_sequences
t = MeCab.Tagger('-Owakati')
PAD = '<PAD>'
UNK = '<UNK>'


def tokenize(text):
    """Tokenize Japanese text.

    Args:
        text: Japanese string.

    Returns:
        A list of words.
    """
    words = t.parse(text).rstrip().split()

    return words


def load_jsonl(jsonl_file):
    """Loads a jsonl file.

    Args:
        jsonl_file: a jsonl file.

    Returns:
        a dictionary.

    Raises:
        json.decoder.JSONDecodeError: if `jsonl_file' is not jsonl format.
    """
    with open(jsonl_file) as f:
        for line in f:
            j = json.loads(line)
            yield j


def input_fn_train(X, y, word_indices, label_indices, maxlen=50, unknown_word_index=1):
    X = [word_indices.doc2idx(document=x, unknown_word_index=unknown_word_index) for x in X]
    X = pad_sequences(X, maxlen=maxlen)
    y = label_indices.doc2idx(document=y)

    return X, y


def input_fn_predict(X, word_indices, maxlen=50, unknown_word_index=1):
    X = [word_indices.doc2idx(document=x, unknown_word_index=unknown_word_index) for x in X]
    X = pad_sequences(X, maxlen=maxlen)

    return X


def load_dataset(jsonl_file):
    X, y = [], []
    for j in load_jsonl(jsonl_file):
        X.append(tokenize(j['text']))
        y.append(j['label'])

    return X, y


def create_dictionary(documents, padding_word_index=None, unknown_word_index=None):
    d = Dictionary(documents)
    # Todo
    if padding_word_index:
        d.token2id = dict((k, v + 1) for k, v in d.token2id.items())
        d.token2id[PAD] = 0
    if unknown_word_index:
        d.token2id = dict((k, v + 1) for k, v in d.token2id.items())
        d.token2id[UNK] = 1

    return d
