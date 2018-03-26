"""
Model Trainer.
"""
import numpy as np
from seqeval.metrics import f1_score, classification_report, accuracy_score
from tqdm import tqdm

from entitypedia.labeling.preprocess import batch_iter


class Trainer(object):

    def __init__(self, model, preprocessor, classes, max_epoch=5, batch_size=32):
        self.model = model
        self.preprocessor = preprocessor
        self.max_epoch = max_epoch
        self.batch_size = batch_size
        self.classes = classes

    def train(self, x_train, y_train, x_valid=None, y_valid=None):
        x_train, y_train = np.asarray(x_train), np.asarray(y_train)
        x_valid, y_valid = np.asarray(x_valid), np.asarray(y_valid)
        num_steps, generator = batch_iter(x_train, y_train, batch_size=self.batch_size,
                                          preprocess=self.preprocessor.transform)
        num_valid_steps, valid_generator = batch_iter(x_valid, y_valid, batch_size=self.batch_size,
                                                      preprocess=self.preprocessor.transform)

        for n in range(self.max_epoch):
            print('Epoch {}/{}'.format(n + 1, self.max_epoch))
            for _ in tqdm(range(num_steps)):
                x, y = generator.__next__()
                self.model.partial_fit(x, y, classes=self.classes)

            print('Validation')
            y_true, y_pred = [], []
            for _ in tqdm(range(num_valid_steps)):
                x, y = valid_generator.__next__()
                y_p = self.model.predict(x)
                y_pred.append(list(y_p))
                y_true.append(y)
            print('- f1: {}'.format(f1_score(y_true, y_pred)))
            print('- accuracy: {}'.format(accuracy_score(y_true, y_pred)))
            print(classification_report(y_true, y_pred))
