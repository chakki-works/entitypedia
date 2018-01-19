"""
Baseline model to classify document.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import numpy as np
from keras.callbacks import TensorBoard
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from entitypedia.classifier.models import build_ffnn
from entitypedia.classifier.utils import create_dictionary, load_dataset


def input_fn_train(X, y, word_indices, label_indices):
    X = [word_indices.doc2bow(document=x) for x in X]
    y = label_indices.doc2idx(document=y)

    return X, y


def main(args):
    print('Loading dataset...')
    X, y = load_dataset(jsonl_file=args.dataset)
    word_dict = create_dictionary(X, padding_word_index=0, unknown_word_index=1)
    label_dict = create_dictionary([y])
    X, y = input_fn_train(X, y, word_dict, label_dict)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42)
    print('Vocabulary: {}'.format(len(word_dict)))

    print('Building the model...')
    model = build_ffnn(len(word_dict), len(label_dict))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    print('Training...')
    model.fit(x_train, y_train, batch_size=args.batch_size, epochs=args.epochs,
              callbacks=[TensorBoard(log_dir=args.log_dir)],
              validation_data=(x_test, y_test))

    print('Evaluating...')
    y_pred = model.predict(x_test, batch_size=args.batch_size)
    y_pred = np.argmax(y_pred, axis=1)
    print(classification_report(y_test, y_pred, target_names=label_dict.values()))


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'dataset1.jsonl'), help='dataset directory')
    parser.add_argument('--pred_data', default=os.path.join(DATA_DIR, 'abstracts.jsonl'), help='dataset directory')
    parser.add_argument('--save_file', default=os.path.join(DATA_DIR, 'article_entity.jsonl'), help='save file')
    parser.add_argument('--model_file', default=os.path.join(DATA_DIR, 'model.h5'), help='file name for model')
    parser.add_argument('--log_dir', default=os.path.join(DATA_DIR, 'logs'), help='log directory')
    parser.add_argument('--word_dic', default=os.path.join(DATA_DIR, 'words.dic'), help='word dictionary')
    parser.add_argument('--label_dic', default=os.path.join(DATA_DIR, 'labels.dic'), help='label dictionary')
    parser.add_argument('--epochs', type=int, default=3, help='number of epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size')
    parser.add_argument('--test_size', type=float, default=0.3, help='batch size')
    args = parser.parse_args()
    main(args)
