"""
Task runner.
"""
import argparse
import os

import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from sklearn.linear_model import SGDClassifier

from entitypedia.labeling.loader import load
from entitypedia.labeling.preprocess import Preprocessor
from entitypedia.labeling.trainer import Trainer


def main(args):
    # Load a dataset and word embedding.
    words, _, labels = load(args.data_path)
    wv_model = KeyedVectors.load(args.embedding_path)

    # Define a model.
    model = SGDClassifier()

    # Prepare a preprocessor.
    preprocess = Preprocessor(word_embeddings=wv_model)
    preprocess.fit(words, labels)
    classes = np.unique(list(preprocess.label_dic.values()))

    # Prepare a trainer.
    trainer = Trainer(model, preprocess, classes=classes)
    trainer.train(words, labels)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--embedding_path', default=os.path.join(DATA_DIR, 'word2vec.gensim.model'))
    parser.add_argument('--data_path', default=os.path.join(DATA_DIR, 'conll.txt'))
    args = parser.parse_args()
    main(args)
