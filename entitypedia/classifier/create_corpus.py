# -*- coding: utf-8 -*-
import fnmatch
import json
import os

SAVE_FILE = 'docs.json'


def list_files(dirname):
    matches = []
    for root, dirnames, filenames in os.walk(dirname):
        for filename in fnmatch.filter(filenames, 'wiki*'):
            matches.append(os.path.join(root, filename))

    return matches


def read_files(filenames):
    for i, filename in enumerate(filenames):
        print('{}/{}'.format(i, len(filenames)))
        with open(filename) as f:
            yield f


def normalize(files):
    docs = {}
    for f in files:
        for line in f:
            if line.startswith('<doc'):
                title = f.readline().strip()
                f.readline()  # skip new line
                abstract = f.readline().strip()
                docs[title] = abstract
    return docs


def save(docs):
    with open(SAVE_FILE, 'w') as f:
        json.dump(docs, f, indent=4)


if __name__ == '__main__':
    dirname = os.path.join(os.path.dirname(__file__), '../data/raw')
    filenames = list_files(dirname)
    files = read_files(filenames)
    texts = normalize(files)
    save(texts)