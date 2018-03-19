import unittest

from entitypedia.classifier.preprocess import remove_tags


class TestUtils(unittest.TestCase):

    def test_remove_tags(self):
        html = 'hoge<a href="fuga">bar</a>buzz'
        cleaned_html = 'hogebarbuzz'
        res = remove_tags(html)
        self.assertEqual(res, cleaned_html)

