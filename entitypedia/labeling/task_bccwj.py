"""
Task runner.
"""
import argparse
import os

import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

from entitypedia.labeling.preprocess import Preprocessor
from entitypedia.labeling.trainer import Trainer
from entitypedia.evaluation.converter import to_iob2
from entitypedia.classifier.preprocess import tokenize


def load(data_path):
    assert os.path.exists(data_path) == True
    remove_types = {'volume', 'period_date', 'percent', 'url', 'service', 'multiplication',
                    'n_person', 'school_age', 'seismic_intensity', 'period_month',
                    'phone_number', 'rank', 'n_animal', 'countx_other', 'point',
                    'periodx_other', 'calorie', 'space', 'period_time', 'n_country',
                    'n_product', 'numex_other', 'latitude_longtitude', 'id_number',
                    'n_flora', 'facility_part', 'temperature', 'weight', 'age', 'water_root',
                    'n_natural_object_other', 'intensity', 'time', 'n_facility',
                    'n_organization', 'postal_address', 'period_year', 'ordinal_number',
                    'physical_extent', 'speed', 'measurement_other', 'seismic_magnitude',
                    'n_event', 'period_week', 'frequency', 'ignored', 'stock', 'n_location_other'}
    X, y = to_iob2(data_path, remove_types)
    docs = [''.join(doc) for doc in X]
    tokenized_docs = [[w for w in tokenize(doc)] for doc in docs]

    tags = []
    for t_doc, doc, label in zip(tokenized_docs, docs, y):
        i = 0
        doc_tags = []
        for word in t_doc:
            j = len(word)
            while not doc[i:].startswith(word):  # correct
                i += 1
            tag = label[i: i + j][0]
            doc_tags.append(tag)
            i += j
        tags.append(doc_tags)

    return tokenized_docs, tags


def main(args):
    # Load a dataset and word embedding.
    words, labels = load(args.data_path)
    X_train, X_test, y_train, y_test = train_test_split(words, labels, test_size=0.3, random_state=42)
    wv_model = KeyedVectors.load(args.embedding_path)

    # Define a model.
    model = SGDClassifier(n_jobs=-1)

    # Prepare a preprocessor.
    preprocess = Preprocessor(window_size=2, word_embeddings=wv_model, vector_size=wv_model.vector_size)
    preprocess.fit(words, labels)
    classes = np.unique(list(preprocess.label_dic.values()))

    # Prepare a trainer.
    trainer = Trainer(model, preprocess, classes=classes, batch_size=100)
    trainer.train(X_train, y_train, X_test, y_test)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--embedding_path', default=os.path.join(DATA_DIR, 'jawiki-embeddings/wiki.ja.word2vec.model'))
    parser.add_argument('--data_path', default=os.path.join(DATA_DIR, '../../../data/raw/corpora/mainichi'))
    args = parser.parse_args()
    main(args)
