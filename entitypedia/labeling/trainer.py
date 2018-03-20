"""
Model Trainer.
"""
import numpy as np
from seqeval.metrics import f1_score, classification_report

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
        num_steps, generator = batch_iter(x_train, y_train, batch_size=self.batch_size,
                                          preprocess=self.preprocessor.transform)

        for n in range(self.max_epoch):
            print('Iteration: {}'.format(n + 1))
            for step in range(num_steps):
                print('  steps: {}'.format(step))
                x, y = generator.__next__()
                self.model.partial_fit(x, y, classes=self.classes)

            # Validation
            y_pred = self.model.predict(x)
            print(f1_score([list(y)], [list(y_pred)]))
            print(classification_report([list(y)], [list(y_pred)]))
