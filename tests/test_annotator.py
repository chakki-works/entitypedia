import unittest
from pprint import pprint

from entitypedia.annotate_named_entity import Annotator


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
