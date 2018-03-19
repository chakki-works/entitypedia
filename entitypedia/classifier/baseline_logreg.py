"""
Baseline model to classify document.
"""
import argparse
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from entitypedia.classifier.utils import tokenize, remove_tags, create_dictionary
from entitypedia.corpora.datasets import DocumentClassifierDataset, load_disambig_ids
from entitypedia.corpora.wikipedia.extractor import save_jsonl, extract_abstract


def load_dataset(wiki_dir, seed_dir):
    X, y = [], []
    dataset = DocumentClassifierDataset(wiki_dir, seed_dir)
    for j in dataset.create():
        try:
            text = extract_abstract(j['text'])
            text = remove_tags(text)
            X.append(text)
            y.append(j['label'])
        except IndexError:
            pass

    return X, y


def load_prediction_dataset(wiki_dir, ignored_ids):
    X, ids = [], []
    dataset = DocumentClassifierDataset(wiki_dir)
    for j in dataset.create_prediction_set(ignored_ids):
        try:
            text = extract_abstract(j['text'])
        except IndexError:
            continue
        text = remove_tags(text)
        id = j['id']
        if id in ignored_ids:
            continue
        X.append(text)
        ids.append(id)

    return X, ids


def main(args):
    print('Loading dataset...')
    X, y = load_dataset(args.wiki_dir, args.seed_dir)
    label_dict = create_dictionary([y])
    y = [label_dict.token2id[y_] for y_ in y]

    print('Vectorizing...')
    vectorizer = TfidfVectorizer(tokenizer=tokenize, analyzer='word')
    X = vectorizer.fit_transform(X)

    print('Fitting...')
    clf = LinearSVC()
    clf.fit(X, y)

    print('Loading dataset for prediction...')
    disambig_ids = load_disambig_ids(args.disambig_file)
    X, ids = load_prediction_dataset(args.wiki_dir, disambig_ids)

    print('Vectorizing...')
    X = vectorizer.transform(X)

    print('Predicting...')
    y_pred = clf.predict(X)

    print('Saving...')
    outputs = [{'id': id, 'ne_id': str(ne_id)} for id, ne_id in zip(ids, y_pred)]
    save_jsonl(outputs, args.save_file)
    label_dict.save(args.label_dic)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw')
    SAVE_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--wiki_dir', default=os.path.join(DATA_DIR, 'extracted'))
    parser.add_argument('--seed_dir', default=os.path.join(DATA_DIR, 'seeds'))
    parser.add_argument('--disambig_file', default=os.path.join(DATA_DIR, 'disambig_id.csv'))
    parser.add_argument('--save_file', default=os.path.join(SAVE_DIR, 'article_entity.jsonl'))
    parser.add_argument('--label_dic', default=os.path.join(SAVE_DIR, 'labels.dic'))
    args = parser.parse_args()
    main(args)
