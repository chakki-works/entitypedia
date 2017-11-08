# -*- coding: utf-8 -*-
import glob
import os
import unittest

from entitypedia.query import QueryBuilder


class TestQueryGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.query_generator = QueryBuilder()

    def test_generate(self):
        template_ptn = os.path.join(os.path.dirname(__file__), '../data/sparql/**/*.rq')
        template_files = glob.glob(template_ptn, recursive=True)  # python 3.6
        for template_file in template_files:
            template_file = template_file.split('data/sparql/')[-1]  # for template engine. Not good!
            query = self.query_generator.build(template_file)
            self.assertIsInstance(query, str)
            self.assertIsNotNone(query)
