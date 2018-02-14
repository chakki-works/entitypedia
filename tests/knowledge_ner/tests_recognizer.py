# -*- coding: utf-8 -*-
import os
import unittest
from pprint import pprint

from knowledge_ner.recognizer import KnowledgeBaseRecognizer
from knowledge_ner.reader import read_csv


class TestRecognizer(unittest.TestCase):

    def setUp(self):
        self.recognizer = KnowledgeBaseRecognizer()
        self.sample_data = os.path.join(os.path.dirname(__file__), 'data/sample.csv')
        # add entity to recognizer
        for entity, label in read_csv(self.sample_data):
            self.recognizer.add_entity(entity, label)

    def test_add_entity(self):
        for entity, label in read_csv(self.sample_data):
            self.assertTrue(self.recognizer.has_entity_of(entity))

    def test_build(self):
        with self.assertRaises(AttributeError):
            self.recognizer.analyze('')

        self.recognizer.build()
        self.recognizer.analyze('')

    def test_analyze(self):
        self.recognizer.build()

        text = '2007年に安倍晋三首相が日本銀行を訪問した。'
        res = self.recognizer.analyze(text)
        pprint(res)
