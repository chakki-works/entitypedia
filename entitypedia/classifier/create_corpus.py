"""
Code for creating a corpus.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import fnmatch
import json
import os

from entitypedia.classifier.utils import *

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


def filter_abstracts(file_abstract, file_seed):
    seeds = dict([(j['id'], j['class']) for j in load_jsonl(file_seed)])
    jsons = load_jsonl(file_abstract)

    for j in jsons:
        id = j['id']
        if id not in seeds:
            continue
        yield {'text': j['text'], 'label': seeds[id]}


if __name__ == '__main__':
    """
    dirname = os.path.join(os.path.dirname(__file__), '../data/raw')
    filenames = list_files(dirname)
    files = read_files(filenames)
    texts = normalize(files)
    save(texts)
    """

    BASE = os.path.join(os.path.dirname(__file__), '../../data/')
    file_seed = os.path.join(BASE, 'seeds.jsonl')
    file_abstract = os.path.join(BASE, 'abstracts.jsonl')
    abstracts = filter_abstracts(file_abstract, file_seed)
    with open('filtered_abstracts.jsonl', 'w') as f:
        for a in abstracts:
            f.write(json.dumps(a))
            f.write('\n')
