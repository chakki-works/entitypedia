import glob
import os

from bs4 import BeautifulSoup

from entitypedia.evaluation.annotator import Annotator


def get_text(text):
    soup = BeautifulSoup(text, 'lxml')
    text = soup.find('text')
    func = lambda s: s.encode('utf-8').decode('utf-8')
    text = ''.join(map(func, text.contents))

    return text


def load_text(file_names, encoding):
    for file_name in file_names:
        with open(file_name, encoding=encoding) as f:
            text = get_text(text=f.read())
            yield text


def to_iob2(dir):
    a = Annotator()
    file_names = glob.glob(os.path.join(dir, '*.sgml'))
    docs = load_text(file_names, encoding='shift_jis')
    X, y = [], []
    for doc in docs:
        text, tags = a.to_bio(doc)
        X.append(text)
        y.append(tags)

    return X, y


if __name__ == '__main__':
    BASE_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw/corpora')
    mainichi_dir = os.path.join(BASE_DIR, 'mainichi')
    bccwj_dir = os.path.join(BASE_DIR, 'bccwj')

    X, y = to_iob2(mainichi_dir)
    print(X[0])
    print(y[0])
