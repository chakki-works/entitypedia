"""
Create datasets.
* Named entity dictionary
* for named entity recognition with conll format
"""
import argparse
import csv
import glob
import os
import re
from collections import namedtuple, defaultdict

from gensim.corpora.dictionary import Dictionary

from entitypedia.corpora.wikipedia.extractor import load_jsonl, save_jsonl
from entitypedia.classifier.utils import tokenize
from entitypedia.corpora.annotator import Annotator


class SeedLoader(object):

    def __init__(self, seed_dir):
        self._dir = seed_dir
        self._seed = namedtuple('Seed', 'title url id image_url abstract type')
        self._seeds = []
        self._id2seed = {}

    def __contains__(self, item):
        return item in self._id2seed

    def __getitem__(self, item):
        return self._id2seed[item]

    def _extract_entity_type(self, file_path):
        idx = file_path.index('seeds/')
        entity_type = file_path[idx + len('seeds/'):][:-4]  # cut .csv

        return entity_type

    def load(self):
        files = glob.glob(os.path.join(self._dir, '**/*.csv'), recursive=True)
        for file in files:
            entity_type = self._extract_entity_type(file)
            with open(file) as f:
                reader = csv.reader(f)
                for line in reader:
                    seed = self._seed(*line+[entity_type])
                    self._seeds.append(seed)
                    self._id2seed[seed.id] = seed


class WikiPageLoader(object):

    def __init__(self, extracted_dir):
        self._dir = extracted_dir
        self._page = namedtuple('Page', 'id url title text')

    def load(self):
        files = glob.glob(os.path.join(self._dir, '**/wiki_*'), recursive=True)
        for jsonl_file in files:
            jsonl = load_jsonl(jsonl_file)
            for json in jsonl:
                page = self._page(**json)

                yield page


class CategoryLoader(object):

    def __init__(self, file):
        self._file = file
        self._id2cat = defaultdict(list)
        self._ptn_num = re.compile(r'\d')
        self._ptn_year = re.compile(r'\d+年')
        self._ptn_pare = re.compile(r'_\(.+\)')

    def __contains__(self, item):
        return item in self._id2cat

    def __getitem__(self, item):
        return self._id2cat[item]

    def _normalize_category(self, text):
        category = self._ptn_num.sub('0', text)
        category = self._ptn_year.sub('0年', category)
        category = self._ptn_pare.sub('', category)
        words = tokenize(category)

        return words[-1]

    def load(self):
        with open(self._file) as f:
            for line in f:
                id, cat = line.strip().split('\t')
                cat = self._normalize_category(cat)
                self._id2cat[id].append(cat)


class DatasetCreator(object):

    def create(self):
        pass


class DocumentClassifierDataset(DatasetCreator):

    def __init__(self, wiki_extracted_dir, seed_dir=''):
        super(DatasetCreator).__init__()
        self._seeds = SeedLoader(seed_dir)
        self._pages = WikiPageLoader(wiki_extracted_dir).load()
        self._seeds.load()

    def create(self):
        for page in self._pages:
            if page.id not in self._seeds:
                continue
            seed = self._seeds[page.id]

            yield {'id': page.id, 'text': page.text, 'label': seed.type}

    def create_prediction_set(self, ignored_ids=()):
        for page in self._pages:
            if page.id in ignored_ids:
                continue
            yield {'id': page.id, 'text': page.text}


class NamedEntityDictionary(DatasetCreator):

    def __init__(self, label_dic, article_entity, wiki_dir, disambig_file):
        super(DatasetCreator).__init__()
        self._title2ne = {}
        self._label_dic = label_dic
        self._article_entity = article_entity
        self._wiki_dir = wiki_dir
        self._disambig_file = disambig_file

    def __contains__(self, item):
        return item in self._title2ne

    def __getitem__(self, item):
        return self._title2ne[item]

    def create(self):
        """Create named entity dictionary.

        Args:
            args: parameters
        """
        # Load files.
        labels = Dictionary.load(self._label_dic)
        article_entity = load_jsonl(self._article_entity)
        pages = WikiPageLoader(self._wiki_dir).load()
        disambig_ids = load_disambig_ids(self._disambig_file)

        # Transform entity id to entity name.
        id2ne = {d['id']: labels[int(d['ne_id'])] for d in article_entity}
        for page in pages:
            if page.id in disambig_ids:
                continue
            if id2ne.get(page.id) == 'concept':
                continue
            if page.id not in id2ne:
                continue
            self._title2ne[page.title] = id2ne[page.id]

        # Todo: include redirect string


def create_iob2data(args):
    """Create named entity recognition dataset with iob2 format.

    Args:
        args: parameters.
    """
    abstracts = load_jsonl(args.abstracts)
    title_entity = load_jsonl(args.title_entity)
    dic = {d['title']: d['type'] for d in title_entity}

    annotator = Annotator(dic=dic)
    with open(args.iob2, 'w') as f:
        total = 0
        error = 0
        for a in abstracts:
            try:
                total += 1
                text, tags = annotator.to_bio(a['abstract'])
            except IndexError:
                error += 1
                continue

            for char, tag in zip(text, tags):
                f.write('{}\t{}\n'.format(char, tag))
            f.write('\n')
    print('{} / {}'.format(error, total))


def load_disambig_ids(file_path):
    with open(file_path) as f:
        ids = {line.strip() for line in f}

    return ids


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'dataset.jsonl'))
    parser.add_argument('--articles', default=os.path.join(DATA_DIR, '../abstracts.jsonl'))
    parser.add_argument('--abstracts', default=os.path.join(DATA_DIR, 'abstracts.jsonl'))
    parser.add_argument('--article_entity', default=os.path.join(DATA_DIR, 'article_entity.jsonl'))
    parser.add_argument('--label_dic', default=os.path.join(DATA_DIR, 'labels.dic'), help='label dictionary')
    parser.add_argument('--disambig_file', default=os.path.join(DATA_DIR, 'disambig_id.csv'), help='disambiguation ids')
    parser.add_argument('--title_entity', default=os.path.join(DATA_DIR, 'title_entity.jsonl'))
    parser.add_argument('--iob2', default=os.path.join(DATA_DIR, 'iob2.tsv'))
    args = parser.parse_args()
    create_iob2data(args)
