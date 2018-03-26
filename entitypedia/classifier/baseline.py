"""
Add Wikipedia's category to feature.
"""
import argparse
import os
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
from scipy.sparse import hstack

from entitypedia.classifier.preprocess import extract_abstract, tokenize, remove_tags, create_dictionary, \
    extract_categories
from entitypedia.corpora.datasets import DocumentClassifierDataset, load_disambig_ids, save_jsonl


def load_dataset(wiki_dir, seed_dir, categories):
    X, y = [], []
    cats = []
    dataset = DocumentClassifierDataset(wiki_dir, seed_dir)
    for j in dataset.create():
        try:
            text = extract_abstract(j['text'])
            text = remove_tags(text)
            X.append(text)
            y.append(j['label'])
            cats.append(' '.join(categories[j['id']]))
        except IndexError:
            pass

    return X, cats, y


def load_prediction_dataset(wiki_dir, ignored_ids, categories):
    X, ids = [], []
    cats = []
    titles = []
    dataset = DocumentClassifierDataset(wiki_dir)
    for j in dataset.create_prediction_set(ignored_ids):
        id = j['id']
        if id in ignored_ids:
            continue
        try:
            text = extract_abstract(j['text'])
        except IndexError:
            continue
        text = remove_tags(text)
        X.append(text)
        ids.append(id)
        cats.append(' '.join(categories[id]))
        titles.append(j['title'])

    return X, cats, ids, titles


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
    X, cats, y = load_dataset(args.wiki_dir, args.seed_dir, categories)
    label_dict = create_dictionary([y])
    y = [label_dict.token2id[y_] for y_ in y]

    print('Vectorizing...')
    vectorizer = TfidfVectorizer(tokenizer=tokenize, analyzer='word')
    X = vectorizer.fit_transform(X)
    category_vectorizer = CountVectorizer()
    cats = category_vectorizer.fit_transform(cats)
    X = hstack([X, cats])

    # x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print('Fitting...')
    clf = LinearSVC()
    clf.fit(X, y)
    # clf.fit(x_train, y_train)

    # print('Predicting...')
    # y_pred = clf.predict(x_test)

    # print('Evaluating...')
    # print(f1_score(y_test, y_pred, average='micro'))
    # print(f1_score(y_test, y_pred, average='macro'))
    # print(classification_report(y_test, y_pred, digits=3))

    print('Loading dataset for prediction...')
    disambig_ids = load_disambig_ids(args.disambig_file)
    X, cats, ids, titles = load_prediction_dataset(args.wiki_dir, disambig_ids, categories)

    print('Vectorizing...')
    X = vectorizer.transform(X)
    cats = category_vectorizer.transform(cats)
    X = hstack([X, cats])

    print('Predicting...')
    y_pred = clf.predict(X)

    print('Saving...')
    outputs = [{'id': int(id), 'ne_id': int(ne_id), 'title': title}
               for id, ne_id, title in zip(ids, y_pred, titles)]
    save_jsonl(outputs, args.save_file)
    label_dict.save(args.label_dic)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw')
    SAVE_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--wiki_dir', default=os.path.join(DATA_DIR, 'extracted'))
    parser.add_argument('--seed_dir', default=os.path.join(DATA_DIR, 'seeds'))
    parser.add_argument('--category', default=os.path.join(DATA_DIR, 'categories.tsv'))
    parser.add_argument('--disambig_file', default=os.path.join(DATA_DIR, 'disambig_id.csv'))
    parser.add_argument('--save_file', default=os.path.join(SAVE_DIR, 'pages.jsonl'))
    parser.add_argument('--label_dic', default=os.path.join(SAVE_DIR, 'labels.dic'))
    args = parser.parse_args()
    main(args)
