# -*- coding: utf-8 -*-
import re
import urllib.parse

from bs4 import BeautifulSoup


class Annotator(object):
    """
    Annotates named-entity tag with Wikipedia text.
    """

    def __init__(self, dic):
        self._regex_link = re.compile(r'<a href="(.+?)">(.+?)</a>')
        self._dic = dic

    def annotate(self, html):
        """Annotates Wikipedia text.

        Args:
            html: html text.

        Return:
            dictionary: annotated text.

        Example:
            >>> html = 'hoge<a href="change">CHANCE</a>fuga<a href="bar">Google</a>'
            >>> annotate(html)
        """
        assert isinstance(html, str)

        links = self._extract_anchor_text(html)
        spans = self._get_link_pos(html)
        spans = self._correct_spans(spans, links)
        clean_text = self._clean_text(html)
        entity_types = self._href2entity_type(links)
        res = self._build_response(clean_text, spans, entity_types)

        return res

    def _get_link_pos(self, html):
        """Gets link positions in html.

        Args:
            html: html text.

        Return:
            list: list of tuples represent link span.

        Example:
            >>> html = 'hoge<a href="change">CHANCE</a>fuga<a href="bar">Google</a>'
            >>> get_link_pos(html)
            [(4, 31), (35, 59)]
        """
        spans = [m.span() for m in self._regex_link.finditer(html)]

        return spans

    def _extract_anchor_text(self, html):
        """Extracts anchor text from html.

        Args:
            html: html text.

        Return:
            list: list of dict. A dict contains href and text.

        Example:
            >>> html = 'hoge<a href="change">CHANCE</a>fuga<a href="bar">Google</a>'
            >>> extract_anchor_text(html)
            [{'href': 'change', 'text': 'CHANCE'},
             {'href': 'bar', 'text': 'Google'}]
        """
        res = []
        for m in self._regex_link.finditer(html):
            href, text = m.groups()
            href = self._decode_url(href)
            res.append({'href': href, 'text': text})

        return res

    def _clean_text(self, html):
        clean_text = BeautifulSoup(html, 'html.parser').text

        return clean_text

    def _correct_spans(self, spans, links):
        """Corrects span corresponding with clean_text.

        Args:
            spans: list of tuples represent link span.
            links: list of dict. A dict contains href and text.

        Return:
            list: list of tuples represent link span.

        Example:
            >>> html = 'hoge<a href="change">CHANCE</a>fuga<a href="bar">Google</a>'
            >>> spans = get_link_pos(html)
            >>> spans
            [(4, 31), (35, 59)]
            >>> links = extract_anchor_text(html)
            >>> clean_text(html)
            'hogeCHANCEfugaGoogle'
            >>> correct_spans(spans, links)
            [(4, 10), (14, 20)]
        """
        acc = 0
        new_spans = []
        for span, link in zip(spans, links):
            text = link['text']
            begin_idx, end_idx = span
            new_spans.append((begin_idx - acc, begin_idx - acc + len(text)))
            acc += end_idx - begin_idx - len(text)

        return new_spans

    def _decode_url(self, percent_encoded_text):
        decoded_text = urllib.parse.unquote(percent_encoded_text)

        return decoded_text

    def _href2entity_type(self, links):
        chunk_types = [self._dic.get(l['href'], 'OTHER') for l in links]

        return chunk_types

    def _build_response(self, clean_text, spans, entity_types):
        res = {
            'text': clean_text,
            'entities': [

            ]
        }

        for (begin_offset, end_offset), entity_type in zip(spans, entity_types):
            entity = {
                'entity': clean_text[begin_offset: end_offset],
                'type': entity_type,
                'beginOffset': begin_offset,
                'endOffset': end_offset
            }
            res['entities'].append(entity)

        return res