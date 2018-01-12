import unittest

from entitypedia.corpora.wikipedia.extractor import extract_abstracts, extract_paragraphs
from entitypedia.corpora.wikipedia.extractor import get_file_list, save_jsonl


class TestExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.files = get_file_list('../data/extracted')

    def test_extract_abstracts(self):
        abstract_file = 'abstracts.jsonl'
        abstracts = extract_abstracts(self.files)
        save_jsonl(abstracts, abstract_file)

    def test_extract_paragraphs(self):
        paragraph_file = 'paragraphs.jsonl'
        paragraphs = extract_paragraphs(self.files)
        save_jsonl(paragraphs, paragraph_file)
