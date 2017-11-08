# -*- coding: utf-8 -*-
from SPARQLWrapper import SPARQLWrapper


class SparqlAPI(object):

    def __init__(self, endpoint='http://ja.dbpedia.org/sparql', return_format='json'):
        self.sparql = SPARQLWrapper(endpoint=endpoint, returnFormat=return_format)

    def run_query(self, query):
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()

        return results
