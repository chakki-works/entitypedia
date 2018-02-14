"""
Baseline model to classify document.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from entitypedia.classifier.utils import tokenize, load_jsonl, remove_tags, create_dictionary
from entitypedia.corpora.wikipedia.extractor import save_jsonl


def load_dataset(jsonl_file):
    X, y = [], []
    for j in load_jsonl(jsonl_file):
        text = remove_tags(j['text'])
        X.append(text)
        y.append(j['label'])

    return X, y


def load_prediction_dataset(jsonl_file):
    X, ids = [], []
    for j in load_jsonl(jsonl_file):
        text = remove_tags(j['abstract'])
        X.append(text)
        ids.append(j['wikipedia_id'])

    return X, ids


def main(args):
    print('Loading dataset...')
    X, y = load_dataset(jsonl_file=args.dataset)
    label_dict = create_dictionary([y])
    y = [label_dict.token2id[y_] for y_ in y]

    print('Vectorizing...')
    vectorizer = TfidfVectorizer(tokenizer=tokenize, analyzer='word')
    X = vectorizer.fit_transform(X)

    print('Fitting...')
    clf = LogisticRegression(penalty='l1', n_jobs=-1)
    clf.fit(X, y)

    print('Loading dataset for prediction...')
    X, ids = load_prediction_dataset(jsonl_file=args.pred_data)

    print('Vectorizing...')
    X = vectorizer.transform(X)

    print('Predicting...')
    y_pred = clf.predict(X)

    print('Saving...')
    outputs = [{'wikipedia_id': id, 'ne_id': str(ne_id)} for id, ne_id in zip(ids, y_pred)]
    save_jsonl(outputs, args.save_file)
    label_dict.save(args.label_dic)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'dataset.jsonl'), help='dataset directory')
    parser.add_argument('--pred_data', default=os.path.join(DATA_DIR, 'abstracts.jsonl'), help='dataset directory')
    parser.add_argument('--save_file', default=os.path.join(DATA_DIR, 'article_entity.jsonl'), help='save file')
    parser.add_argument('--label_dic', default=os.path.join(DATA_DIR, 'labels.dic'), help='label dictionary')
    args = parser.parse_args()
    main(args)
