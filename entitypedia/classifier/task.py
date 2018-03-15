"""
Add Wikipedia's category to feature.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import csv
import os
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
from scipy.sparse import hstack

from entitypedia.classifier.utils import tokenize, load_jsonl, remove_tags, create_dictionary
from entitypedia.corpora.wikipedia.extractor import save_jsonl, extract_categories


def load_dataset(jsonl_file, categories):
    X, y = [], []
    cats = []
    for j in load_jsonl(jsonl_file):
        text = remove_tags(j['text'])
        id = j['id']
        X.append(text)
        y.append(j['label'])
        cats.append(' '.join(categories[id]))

    return X, cats, y


def load_prediction_dataset(jsonl_file, remove_ids):
    X, ids = [], []
    for j in load_jsonl(jsonl_file):
        text = remove_tags(j['abstract'])
        id = j['wikipedia_id']
        if id in remove_ids:
            continue
        X.append(text)
        ids.append(id)

    return X, ids


def load_disambig_ids(file_path):
    with open(file_path) as f:
        ids = {line.strip() for line in f}

    return ids


def load_categories(file_path):
    with open(file_path) as f:
        lines = [line.strip().split('\t') for line in f]
    ids, cats = [], []
    for row in lines:
        ids.append(row[0])
        cats.append(row[1])
    cats = extract_categories(cats)
    res = defaultdict(list)
    for id, cat in zip(ids, cats):
        res[id].append(cat)

    return res


def main(args):
    print('Loading dataset...')
    categories = load_categories(args.category)
    X, cats, y = load_dataset(args.dataset, categories)
    label_dict = create_dictionary([y])
    y = [label_dict.token2id[y_] for y_ in y]

    print('Vectorizing...')
    vectorizer = TfidfVectorizer(tokenizer=tokenize, analyzer='word')
    X = vectorizer.fit_transform(X)
    category_vectorizer = CountVectorizer()
    cats = category_vectorizer.fit_transform(cats)
    X = hstack([X, cats])

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print('Fitting...')
    clf = LinearSVC()
    clf.fit(X, y)

    print('Predicting...')
    y_pred = clf.predict(x_test)

    print('Evaluating...')
    print(f1_score(y_test, y_pred, average='micro'))
    print(f1_score(y_test, y_pred, average='macro'))
    print(classification_report(y_test, y_pred, digits=3))

    """
    print('Loading dataset for prediction...')
    disambig_ids = load_disambig_ids(args.disambig_file)
    X, ids = load_prediction_dataset(args.pred_data, disambig_ids)

    print('Vectorizing...')
    X = vectorizer.transform(X)

    print('Predicting...')
    y_pred = clf.predict(X)

    print('Saving...')
    outputs = [{'wikipedia_id': id, 'ne_id': str(ne_id)} for id, ne_id in zip(ids, y_pred)]
    save_jsonl(outputs, args.save_file)
    label_dict.save(args.label_dic)
    """


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'dataset.jsonl'), help='dataset directory')
    parser.add_argument('--category', default=os.path.join(DATA_DIR, 'categories.tsv'), help='category file')
    parser.add_argument('--pred_data', default=os.path.join(DATA_DIR, 'abstracts.jsonl'), help='dataset directory')
    parser.add_argument('--save_file', default=os.path.join(DATA_DIR, 'article_entity.jsonl'), help='save file')
    parser.add_argument('--label_dic', default=os.path.join(DATA_DIR, 'labels.dic'), help='label dictionary')
    parser.add_argument('--disambig_file', default=os.path.join(DATA_DIR, 'disambig_id.csv'), help='disambiguation ids')
    args = parser.parse_args()
    main(args)
