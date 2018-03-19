"""
Create datasets.
* Named entity dictionary
* for named entity recognition with conll format
"""
import argparse
import csv
import glob
import os
from collections import namedtuple

from gensim.corpora.dictionary import Dictionary

from entitypedia.corpora.wikipedia.extractor import load_jsonl, save_jsonl
from entitypedia.classifier.baseline_logreg import load_disambig_ids
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

    def __init__(self):
        pass

    def load(self):
        pass


class DatasetCreator(object):

    def create(self):
        pass


class DocumentClassifierDataset(DatasetCreator):

    def __init__(self, wiki_extracted_dir, seed_dir):
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


class NamedEntityDataset(object):

    def __init__(self):
        super(DatasetCreator).__init__()


def create_named_entity_dictionary(args):
    """Create named entity dictionary.

    Args:
        args: parameters
    """
    # Load files.
    labels = Dictionary.load(args.label_dic)
    article_entity = load_jsonl(args.article_entity)
    articles = load_jsonl(args.articles)
    disambig_ids = load_disambig_ids(args.disambig_file)

    # Transform entity id to entity name.
    id2ne = {d['wikipedia_id']: labels[int(d['ne_id'])] for d in article_entity}
    title2ne = [{'title': d['title'], 'type': id2ne[d['id']]} for d in articles
                if d['id'] not in disambig_ids and id2ne.get(d['id']) != 'concept' and d['id'] in id2ne]

    # Save named entity dictionary.
    save_jsonl(title2ne, args.title_entity)


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
    create_named_entity_dictionary(args)
    create_iob2data(args)
