# -*- coding: utf-8 -*-
from collections import defaultdict

import ahocorasick


class KnowledgeBaseRecognizer(object):

    def __init__(self):
        self._dictionary = ahocorasick.Automaton()
        self._labels = {}
        self._entity2detail = {}

    def add_entity(self, entity, label):
        self._dictionary.add_word(entity,
                                  (len(self._dictionary), entity))
        self._labels[entity] = label

    def add_word(self, entity, sub_type, page_url, image_url):
        self._entity2detail[entity] = {'sub_type': sub_type,
                                       'page_url': page_url,
                                       'img_url': image_url}

    def has_entity_of(self, entity):
        return entity in self._dictionary

    def build(self):
        self._dictionary.make_automaton()

    def analyze(self, sent):
        chunks = self._get_chunks(sent)
        chunks = self._filter_chunks(chunks)
        res = self._build_response(sent, chunks)

        return res

    def iob2(self, sent):
        chunks = self._get_chunks(sent)
        chunks = self._filter_chunks(chunks)
        res = self._build_iob2(chunks, length=len(sent))

        return res

    def _build_iob2(self, chunks, length):
        res = ['O'] * length
        for chunk_start, chunk_end, entity in chunks:
            for i in range(chunk_start, chunk_end):
                prefix = 'B' if i == chunk_start else 'I'
                # type_ = self._labels[entity]
                type_ = self._entity2detail[entity]['sub_type']
                res[i] = '{}-{}'.format(prefix, type_)

        return res

    def _get_chunks(self, sent):
        for idx, (_, w) in self._dictionary.iter(sent):
            end_idx = idx + 1
            start_idx = end_idx - len(w)
            yield start_idx, end_idx, w

    def _filter_chunks(self, chunks):
        chunks = sorted(chunks)
        # print(chunks)
        # 開始位置が同じなら最も長い単語を残す
        dic = defaultdict(list)
        for chunk in chunks:
            start_idx = chunk[0]
            dic[start_idx].append(chunk)
        chunks = sorted(max(ls) for ls in dic.values())
        # print(chunks)

        max_idx = 0
        for start_idx, end_idx, w in chunks:
            if start_idx >= max_idx:
               yield start_idx, end_idx, w
               max_idx = end_idx

    def _build_response(self, sent, chunks):
        res = {
            'text': sent,
            'entities': [

            ]
        }
        for chunk_start, chunk_end, entity in chunks:
            entity = {
                'text': entity,
                'type': self._labels[entity],
                'beginOffset': chunk_start,
                'endOffset': chunk_end,
                'disambiguation': {
                    'sub_type': self._entity2detail[entity]['sub_type'],
                    'page_url': self._entity2detail[entity]['page_url'],
                    'img_url': self._entity2detail[entity]['img_url']
                }
            }
            res['entities'].append(entity)

        return res
