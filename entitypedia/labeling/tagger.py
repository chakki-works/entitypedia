"""
Model API.
"""
from seqeval.metrics.sequence_labeling import get_entities


class Tagger(object):

    def __init__(self, model, preprocessor=None, tokenizer=str.split):
        self.model = model
        self.preprocessor = preprocessor
        self.tokenizer = tokenizer

    def predict(self, sent):
        """Predict using the model.

        Args:
            sent : string, the input data.
        Returns:
           y_pred : array-like, the predicted classes.
        """
        y_pred = []

        words = self.tokenizer(sent)
        X = self.preprocessor.transform([words])
        for feature in X:
            y = self.model.predict([feature])
            y_pred.append(y[0])

        return y_pred

    def _build_response(self, sent, tags):
        words = self.tokenizer(sent)
        res = {
            'words': words,
            'entities': [

            ]
        }
        chunks = get_entities(tags)

        for chunk_type, chunk_start, chunk_end in chunks:
            chunk_end += 1
            entity = {
                'text': ' '.join(words[chunk_start: chunk_end]),
                'type': chunk_type,
                'beginOffset': chunk_start,
                'endOffset': chunk_end
            }
            res['entities'].append(entity)

        return res

    def analyze(self, sent):
        assert isinstance(sent, str)

        tags = self.predict(sent)
        res = self._build_response(sent, tags)

        return res


if __name__ == '__main__':
    import os
    import argparse
    from pprint import pprint
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--embedding_path', default=os.path.join(DATA_DIR, 'word2vec.gensim.model'))
    parser.add_argument('--data_path', default=os.path.join(DATA_DIR, 'conll.txt'))
    args = parser.parse_args()

    import numpy as np
    from gensim.models.keyedvectors import KeyedVectors
    from sklearn.linear_model import SGDClassifier

    from entitypedia.labeling.loader import load
    from entitypedia.labeling.preprocess import Preprocessor, tokenize
    from entitypedia.labeling.trainer import Trainer

    # Load a dataset and word embedding.
    words, _, labels = load(args.data_path)
    wv_model = KeyedVectors.load(args.embedding_path)

    # Define a model.
    model = SGDClassifier()

    # Prepare a preprocessor.
    preprocess = Preprocessor(word_embeddings=wv_model)
    preprocess.fit(words, labels)
    classes = np.unique(list(preprocess.label_dic.values()))

    # Prepare a trainer.
    trainer = Trainer(model, preprocess, classes=classes)
    trainer.train(words, labels)

    tagger = Tagger(model, preprocess, tokenize)
    while True:
        sent = input('Input sentence: ')
        print(tagger.predict(sent))
        pprint(tagger.analyze(sent))
