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

from entitypedia.classifier.utils import input_fn_predict, load_prediction_dataset
from entitypedia.corpora.wikipedia.extractor import save_jsonl


def main(args):
    # Load datasets, model and dictionaries.
    X, ids = load_prediction_dataset(jsonl_file=args.dataset)
    word_dict = Dictionary.load(args.word_dic)
    model = load_model(args.model_file)
    X = input_fn_predict(X, word_dict)

    # Predict label.
    y_pred = model.predict(X, batch_size=args.batch_size)
    y_pred = np.argmax(y_pred, axis=1)

    outputs = []
    for id, ne_id in zip(ids, y_pred):
        outputs.append({'wikipedia_id': id, 'ne_id': str(ne_id)})
    save_jsonl(outputs, args.save_file)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Code for prediction')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'abstracts.jsonl'), help='dataset directory')
    parser.add_argument('--save_file', default=os.path.join(DATA_DIR, 'article_entity.jsonl'), help='save file')
    parser.add_argument('--model_file', default=os.path.join(DATA_DIR, 'model.h5'), help='file name for model')
    parser.add_argument('--word_dic', default=os.path.join(DATA_DIR, 'words.dic'), help='word dictionary')
    parser.add_argument('--label_dic', default=os.path.join(DATA_DIR, 'labels.dic'), help='label dictionary')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size')
    args = parser.parse_args()
    main(args)
