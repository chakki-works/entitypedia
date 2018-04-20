import csv
import os
import re
import unittest

from entitypedia.corpora.datasets import SeedLoader, WikiPageLoader, CategoryLoader, save_jsonl
from entitypedia.corpora.datasets import DocumentClassifierDataset, NamedEntityDictionary
from entitypedia.corpora.datasets import save_jsonl

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')


class TestSeedLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dir = os.path.join(DATA_DIR, 'seeds')

    def test_load(self):
        seeds = SeedLoader(self.dir)
        seeds.load()

        self.assertIsInstance(seeds._id2seed, dict)
        self.assertIsInstance(seeds._seeds, list)
        self.assertEqual(len(seeds._seeds), 10)

    def test_seed_sampling(self):
        seed_dir = os.path.join(os.path.dirname(__file__), '../../data/raw/seeds')
        save_dir = os.path.join(os.path.dirname(__file__), '../../data/interim/')
        seeds = SeedLoader(seed_dir)
        seeds.load()
        seed_per_type = seeds.sample()
        with open(os.path.join(save_dir, 'seeds.csv'), 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for entity_type, seeds in seed_per_type.items():
                for seed in seeds:
                    writer.writerow([entity_type, seed.title, seed.id])


class TestWikiPageLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dir = os.path.join(DATA_DIR, 'extracted')

    def test_load(self):
        loader = WikiPageLoader(self.dir)
        pages = loader.load()

        self.assertEqual(len(list(pages)), 11)


class TestCategoryLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = os.path.join(DATA_DIR, 'categories.tsv')

    def test_load(self):
        loader = CategoryLoader(self.file)
        loader.load()

        self.assertEqual(len(loader._id2cat), 7)


class TestDocumentClassifierDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.seed_dir = os.path.join(DATA_DIR, 'seeds')
        cls.wiki_dir = os.path.join(DATA_DIR, 'extracted')

    def setUp(self):
        self.dataset = DocumentClassifierDataset(self.wiki_dir, self.seed_dir)

    def test_create(self):
        generator = self.dataset.create()
        self.assertEqual(len(list(generator)), 0)

    def test_create_prediction(self):
        generator = self.dataset.create_prediction_set()
        self.assertEqual(len(list(generator)), 11)


class TestNamedEntityDictionary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
        cls.wiki_dir = os.path.join(cls.DATA_DIR, 'raw/extracted')
        cls.disambig_file = os.path.join(cls.DATA_DIR, 'raw/disambig_id.csv')
        cls.label_file = os.path.join(cls.DATA_DIR, 'interim/labels.dic')
        cls.article_entity = os.path.join(cls.DATA_DIR, 'interim/article_entity.jsonl')

    def setUp(self):
        self.dictionary = NamedEntityDictionary(self.label_file, self.article_entity, self.disambig_file)

    def test_create(self):
        self.dictionary.create()

        file = os.path.join(self.DATA_DIR, 'interim/title_entity.jsonl')
        objs = [{k: v} for k, v in self.dictionary._title2ne.items()]
        save_jsonl(objs, file)

    def test_create_wiki_sents(self):
        data_dir = os.path.join(os.path.dirname(__file__), '../../data')
        dir = os.path.join(data_dir, 'extracted')
        save_file = os.path.join(data_dir, 'interim/wiki_sents.txt')
        loader = WikiPageLoader(dir)
        pages = loader.load()
        with open(save_file, 'w') as f:
            for page in pages:
                sents = re.split(r'\n|。', page.text)
                for i, sent in enumerate(sents[1:], 1):
                    if sent == '':
                        continue
                    if 'a href' in sent:
                        f.write('{}\n'.format(sent))
