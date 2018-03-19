import os
import unittest

from entitypedia.corpora.datasets import SeedLoader, WikiPageLoader, CategoryLoader
from entitypedia.corpora.datasets import DocumentClassifierDataset, NamedEntityDataset

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


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
        cls.file = os.path.join(DATA_DIR, 'raw/categories.tsv')

    def test_load(self):
        loader = CategoryLoader(self.file)
        loader.load()


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
