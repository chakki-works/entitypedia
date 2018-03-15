# -*- coding: utf-8 -*-
"""
Code for extracting text from WikiExtractor's output.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import json
import os
import re

from entitypedia.classifier.utils import load_jsonl, tokenize


def extract_paragraph(text):
    """Extracts Wikipedia's paragraphs.

    Args:
        text: WikiExtractor's output text.

    Returns:
        A list of paragraph(str).
    """
    # paragraph[0] is article's title.
    paragraphs = [p for p in text.split('\n') if p != '']

    return paragraphs


def extract_abstract(text):
    """Extracts Wikipedia's abstract.

    Args:
        text: WikiExtractor's output text.

    Returns:
        abstract text.

    Raises:
        IndexError: if abstract is null.
    """
    paragraphs = extract_paragraph(text)

    return paragraphs[1]


def extract_abstracts(files):
    pass_count = 0
    for file in files:
        jsonl = load_jsonl(file)
        for j in jsonl:
            try:
                abstract = extract_abstract(j['text'])
                yield {'wikipedia_id': j['id'], 'abstract': abstract}
            except IndexError:
                pass_count += 1

    print('Passed: {}'.format(pass_count))


def extract_paragraphs(files):
    for file in files:
        jsonl = load_jsonl(file)
        for j in jsonl:
            paragraphs = extract_paragraph(j['text'])
            for p_id, p in enumerate(paragraphs[1:]):
                yield {'wikipedia_id': j['id'], 'paragraph_id': p_id, 'text': p}


def save_jsonl(objs, file_name):
    """Save objs into a jsonl file.

    Args:
        objs: iterator object.
        file_name: a jsonl file.

    Raises:
        TypeError: if `objs' is not iterable.
    """
    with open(file_name, 'w') as f:
        for obj in objs:
            json.dump(obj, f)
            f.write('\n')


def get_file_list(dir_name):
    """Gets WikiExtractor's output file list.

    Args:
        dir_name: output directory name.

    Returns:
        A list of file names.
    """
    file_list = glob.glob(os.path.join(dir_name, '**/wiki_*'), recursive=True)

    return file_list


def filter_docs(docs, ids):
    """Filter docs by ID.

    Args:
        docs: A list of doc.
        ids: Set of wikipedia id.

    Returns:
        A list of dictionary.
    """
    for doc in docs:
        if doc['wikipedia_id'] not in ids:
            continue
        yield doc


def create_dataset_for_classifier(doc_file, seed_file):
    docs = load_jsonl(doc_file)
    seeds = load_jsonl(seed_file)
    seed_ids = {s['id']: s['class'] for s in seeds}
    filtered_docs = filter_docs(docs, seed_ids)
    for d in filtered_docs:
        id = d['wikipedia_id']
        yield {'text': d['abstract'], 'label': seed_ids[id], 'id': id}


def extract_categories(categories):
    res = []
    pattern = re.compile(r'\d')
    ptn_year = re.compile(r'\d+年')
    ptn_pare = re.compile(r'_\(.+\)')
    for category in categories:
        category = pattern.sub('0', category)
        category = ptn_year.sub('0年', category)
        category = ptn_pare.sub('', category)
        words = tokenize(category)
        res.append(words[-1])

    return res
