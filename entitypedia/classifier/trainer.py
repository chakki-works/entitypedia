"""
Code for training a model classifies Wikipedia abstract into named-entity type.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os

import numpy as np
from keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from entitypedia.classifier.models import build_model
from entitypedia.classifier.utils import input_fn_train, create_dictionary, load_dataset


def main(args):
    # Load datasets.
    X, y = load_dataset(jsonl_file=args.dataset)
    word_dict = create_dictionary(X, padding_word_index=0, unknown_word_index=1)
    label_dict = create_dictionary([y])
    X, y = input_fn_train(X, y, word_dict, label_dict)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42)

    # Build the model.
    model = build_model(len(word_dict), len(label_dict))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # Train the model.
    model.fit(x_train, y_train, batch_size=args.batch_size, epochs=args.epochs,
              callbacks=[TensorBoard(log_dir=args.log_dir)],
              validation_data=(x_test, y_test))

    # Evaluate accuracy over one epoch of test_set.
    y_pred = model.predict(x_test, batch_size=args.batch_size)
    y_pred = np.argmax(y_pred, axis=1)
    print(classification_report(y_test, y_pred, target_names=label_dict.values()))

    # Save the model and dictionaries.
    model.save(args.model_file)
    word_dict.save(args.word_dic)
    label_dict.save(args.label_dic)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/interim')
    parser = argparse.ArgumentParser(description='Training a classifier')
    parser.add_argument('--dataset', default=os.path.join(DATA_DIR, 'dataset.jsonl'), help='dataset directory')
    parser.add_argument('--log_dir', default=os.path.join(DATA_DIR, 'logs'), help='log directory')
    parser.add_argument('--model_file', default=os.path.join(DATA_DIR, 'model.h5'), help='file name for model')
    parser.add_argument('--word_dic', default=os.path.join(DATA_DIR, 'words.dic'), help='word dictionary')
    parser.add_argument('--label_dic', default=os.path.join(DATA_DIR, 'labels.dic'), help='label dictionary')
    parser.add_argument('--epochs', type=int, default=3, help='number of epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size')
    parser.add_argument('--test_size', type=float, default=0.3, help='batch size')
    args = parser.parse_args()
    main(args)
