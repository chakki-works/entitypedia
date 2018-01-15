"""
Code for prediction.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import numpy as np
from gensim.corpora.dictionary import Dictionary
from keras.models import load_model

from entitypedia.classifier.utils import input_fn_predict, load_dataset


def main(args):
    # Load datasets, model and dictionaries.
    X, _ = load_dataset(jsonl_file=args.dataset)
    word_dict = Dictionary.load(args.word_dic)
    model = load_model(args.model_file)
    X = input_fn_predict(X, word_dict)

    # Predict label.
    y_pred = model.predict(X, batch_size=args.batch_size)
    y_pred = np.argmax(y_pred, axis=1)

    # Todo: Save y_pred and article ID.


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
    parser = argparse.ArgumentParser(description='Code for prediction')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'dataset.jsonl'), help='dataset directory')
    parser.add_argument('--model_file', default=os.path.join(DATA_DIR, 'model.h5'), help='file name for model')
    parser.add_argument('--word_dic', default=os.path.join(DATA_DIR, 'words.dic'), help='word dictionary')
    parser.add_argument('--label_dic', default=os.path.join(DATA_DIR, 'labels.dic'), help='label dictionary')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size')
    args = parser.parse_args()
    main(args)
