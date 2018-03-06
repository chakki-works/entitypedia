# -*- coding: utf-8 -*-
import os
import unittest
from pprint import pprint

from gensim.corpora.dictionary import Dictionary
from entitypedia.classifier.utils import load_jsonl

from entitypedia.corpora.annotator import Annotator


class TestAnnotator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dic = {'bar': 'Organization', 'ラテン語': 'Language'}
        cls.annotator = Annotator(dic)
        cls.html = 'hoge<a href="change">CHANCE</a>fuga<a href="bar">Google</a>'

    def test_get_link_pos(self):
        spans = self.annotator._get_link_pos(self.html)
        self.assertIsInstance(spans, list)
        for span in spans:
            self.assertIsInstance(span, tuple)
            self.assertEqual(len(span), 2)
            for num in span:
                self.assertIsInstance(num, int)
            self.assertLess(span[0], span[1])

    def test_extract_anchor_text(self):
        links = self.annotator._extract_anchor_text(self.html)
        self.assertIsInstance(links, list)
        for link in links:
            self.assertIsInstance(link, dict)
            self.assertEqual(len(link), 2)
            self.assertIn('href', link)
            self.assertIn('text', link)
            self.assertIsInstance(link['href'], str)
            self.assertIsInstance(link['text'], str)

    def test_correct_spans(self):
        spans = self.annotator._get_link_pos(self.html)
        links = self.annotator._extract_anchor_text(self.html)
        true_spans = [(4, 31), (35, 59)]
        self.assertEqual(spans, true_spans)

        spans = self.annotator._correct_spans(spans, links)
        true_spans = [(4, 10), (14, 20)]
        self.assertEqual(spans, true_spans)

    def test_annotate(self):
        html = """アンパサンドを意味する <a href=\"%E8%A8%98%E5%8F%B7\">記号</a>である。<a href=\"%E3%83%A9%E3%83%86%E3%83%B3%E8%AA%9E\">ラテン語</a>の<a href=\"%E5%90%88%E5%AD%97\">合字</a>"""

        annotated = self.annotator.annotate(html)
        pprint(annotated)
        text = annotated['text']
        for e in annotated['entities']:
            i, j = e['beginOffset'], e['endOffset']
            self.assertEqual(text[i: j], e['entity'])

        html = """羅臼岳（らうすだけ）は、<a href="%E5%8C%97%E6%B5%B7%E9%81%93">北海道</a>・<a href="%E7%9F%A5%E5%BA%8A%E5%8D%8A%E5%B3%B6">知床半島</a>にある<a href="%E7%81%AB%E5%B1%B1">火山</a>群の主峰及び最高峰で<a href="%E6%A8%99%E9%AB%98">標高</a>1,661m<ref name="gsi.go.jp/common/000091072"></ref>。古くは<a href="%E3%82%A2%E3%82%A4%E3%83%8C%E8%AA%9E">アイヌ語</a>でチャチャヌプリ、また良牛岳と記されたこともある。<a href="1964%E5%B9%B4">1964年</a>（昭和39年）<a href="6%E6%9C%881%E6%97%A5">6月1日</a>に<a href="%E7%9F%A5%E5%BA%8A%E5%9B%BD%E7%AB%8B%E5%85%AC%E5%9C%92">知床国立公園</a>に指定され、<a href="2005%E5%B9%B4">2005年</a>7月にこの山域を含む知床半島が<a href="%E7%9F%A5%E5%BA%8A%20%28%E4%B8%96%E7%95%8C%E9%81%BA%E7%94%A3%29">知床 (世界遺産)</a>に正式登録された。<a href="%E6%97%A5%E6%9C%AC%E7%99%BE%E5%90%8D%E5%B1%B1">日本百名山</a>、<a href="%E8%8A%B1%E3%81%AE%E7%99%BE%E5%90%8D%E5%B1%B1">花の百名山</a>及び<a href="%E6%96%B0%E3%83%BB%E8%8A%B1%E3%81%AE%E7%99%BE%E5%90%8D%E5%B1%B1">新・花の百名山</a>に選定されている山である。"""
        # html = """羅臼岳（らうすだけ）は、<a href="%E5%8C%97%E6%B5%B7%E9%81%93">北海道</a>・<a href="%E7%9F%A5%E5%BA%8A%E5%8D%8A%E5%B3%B6">知床半島</a>にある<a href="%E7%81%AB%E5%B1%B1">火山</a>群の主峰及び最高峰で<a href="%E6%A8%99%E9%AB%98">標高</a>1,661m。古くは<a href="%E3%82%A2%E3%82%A4%E3%83%8C%E8%AA%9E">アイヌ語</a>でチャチャヌプリ、また良牛岳と記されたこともある。<a href="1964%E5%B9%B4">1964年</a>（昭和39年）<a href="6%E6%9C%881%E6%97%A5">6月1日</a>に<a href="%E7%9F%A5%E5%BA%8A%E5%9B%BD%E7%AB%8B%E5%85%AC%E5%9C%92">知床国立公園</a>に指定され、<a href="2005%E5%B9%B4">2005年</a>7月にこの山域を含む知床半島が<a href="%E7%9F%A5%E5%BA%8A%20%28%E4%B8%96%E7%95%8C%E9%81%BA%E7%94%A3%29">知床 (世界遺産)</a>に正式登録された。<a href="%E6%97%A5%E6%9C%AC%E7%99%BE%E5%90%8D%E5%B1%B1">日本百名山</a>、<a href="%E8%8A%B1%E3%81%AE%E7%99%BE%E5%90%8D%E5%B1%B1">花の百名山</a>及び<a href="%E6%96%B0%E3%83%BB%E8%8A%B1%E3%81%AE%E7%99%BE%E5%90%8D%E5%B1%B1">新・花の百名山</a>に選定されている山である。"""
        annotated = self.annotator.annotate(html)
        pprint(annotated)
        text = annotated['text']
        for e in annotated['entities']:
            i, j = e['beginOffset'], e['endOffset']
            self.assertEqual(text[i: j], e['entity'])

    def test_annotate_entity(self):
        data_dir = os.path.join(os.path.dirname(__file__), '../data/interim/')
        labels = Dictionary.load(os.path.join(data_dir, 'labels.dic'))
        article_entity = load_jsonl(os.path.join(data_dir, 'article_entity.jsonl'))
        abstracts = load_jsonl(os.path.join(data_dir, 'abstracts.jsonl'))
        articles = load_jsonl(os.path.join(data_dir, '../abstracts.jsonl'))

        id2ne = {d['wikipedia_id']: labels[int(d['ne_id'])] for d in article_entity}
        title2ne = {d['title']: id2ne.get(d['id'], 'other') for d in articles}
        annotator = Annotator(dic=title2ne)
        for i, a in enumerate(abstracts):
            if i == 100:
                break
            pprint(annotator.annotate(a['abstract']))

    def load_concept(self, file):
        import csv
        with open(file) as f:
            reader = csv.reader(f)
            ids = {row[2] for row in reader}
        return ids

    def test_create_dictionary(self):
        """
        固有表現認識用の辞書を作成する
        """
        data_dir = os.path.join(os.path.dirname(__file__), '../data/interim/')
        labels = Dictionary.load(os.path.join(data_dir, 'labels.dic'))
        article_entity = load_jsonl(os.path.join(data_dir, 'article_entity.jsonl'))
        abstracts = load_jsonl(os.path.join(data_dir, 'abstracts.jsonl'))
        articles = load_jsonl(os.path.join(data_dir, '../abstracts.jsonl'))
        from entitypedia.classifier.baseline_logreg import load_disambig_ids
        disambig_ids = load_disambig_ids(os.path.join(data_dir, 'disambig_id.csv'))
        concept_ids = self.load_concept(os.path.join(os.path.dirname(__file__), '../data/raw/seeds/concept.csv'))
        remove_ids = disambig_ids | concept_ids

        id2ne = {d['wikipedia_id']: labels[int(d['ne_id'])] for d in article_entity}
        title2ne = [{d['title']: id2ne.get(d['id'], 'other')} for d in articles if d['id'] not in remove_ids]
        from entitypedia.corpora.wikipedia.extractor import save_jsonl
        save_file = os.path.join(data_dir, 'title_entity.jsonl')
        save_jsonl(title2ne, save_file)

    def test_bio(self):
        data_dir = os.path.join(os.path.dirname(__file__), '../data/interim/')
        labels = Dictionary.load(os.path.join(data_dir, 'labels.dic'))
        article_entity = load_jsonl(os.path.join(data_dir, 'article_entity.jsonl'))
        abstracts = load_jsonl(os.path.join(data_dir, 'abstracts.jsonl'))
        articles = load_jsonl(os.path.join(data_dir, '../abstracts.jsonl'))

        id2ne = {d['wikipedia_id']: labels[int(d['ne_id'])] for d in article_entity}
        title2ne = {d['title']: id2ne.get(d['id'], 'other') for d in articles}
        annotator = Annotator(dic=title2ne)
        f = open('dataset.tsv', 'w')
        total = 0
        error = 0
        for i, a in enumerate(abstracts):
            try:
                total += 1
                text, tags = annotator.to_bio(a['abstract'])
            except IndexError:
                error += 1
                continue

            for char, tag in zip(text, tags):
                f.write('{}\t{}\n'.format(char, tag))
            f.write('\n')
        f.close()
        print('{} / {}'.format(error, total))
