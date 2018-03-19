"""
Preprocessor.
"""
import re

import MeCab
from bs4 import BeautifulSoup
from gensim.corpora.dictionary import Dictionary
PAD = 'PAD'
UNK = 'UNK'

t = MeCab.Tagger('-Owakati')


def extract_paragraph(text):
    """Extracts Wikipedia's paragraphs.

    Args:
        text: WikiExtractor's output text.

    Returns:
        A list of paragraph(str).
    """
    # paragraph[0] is article's title.
    paragraphs = [p for p in text.split('\n') if p != '']

    return paragraphs


def extract_abstract(text):
    """Extracts Wikipedia's abstract.

    Args:
        text: WikiExtractor's output text.

    Returns:
        abstract text.

    Raises:
        IndexError: if abstract is null.
    """
    paragraphs = extract_paragraph(text)

    return paragraphs[1]


def tokenize(text):
    """Tokenize Japanese text.

    Args:
        text: Japanese string.

    Returns:
        A list of words.
    """
    words = t.parse(text).rstrip().split()

    return words


def remove_tags(html):
    """Remove all html tags.

    Args:
        html: html string.

    Returns:
        cleaned text.

    Example:
        >>> html = 'hoge<a href="fuga">bar</a>buzz'
        >>> remove_tags(html)
        hogebarbuzz
    """
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    return text


def create_dictionary(documents, padding_word_index=None, unknown_word_index=None, prune_at=None):
    if prune_at:
        d = Dictionary(documents, prune_at=prune_at)
    else:
        d = Dictionary(documents)
    # Todo
    if padding_word_index:
        d.token2id = dict((k, v + 1) for k, v in d.token2id.items())
        d.token2id[PAD] = 0
    if unknown_word_index:
        d.token2id = dict((k, v + 1) for k, v in d.token2id.items())
        d.token2id[UNK] = 1

    return d


def extract_categories(categories):
    res = []
    pattern = re.compile(r'\d')
    ptn_year = re.compile(r'\d+年')
    ptn_pare = re.compile(r'_\(.+\)')
    for category in categories:
        category = pattern.sub('0', category)
        category = ptn_year.sub('0年', category)
        category = ptn_pare.sub('', category)
        words = tokenize(category)
        res.append(words[-1])

    return res