import os

import numpy as np
from sklearn.model_selection import train_test_split

from models import build_model
from utils import *


if __name__ == '__main__':
    save_path = './dictionary.json'
    file_path = os.path.join(os.path.dirname(__file__), '../../data/category_class.jsonl')
    word_indices, label_indices = maybe_create_indices(file_path, save_path)

    vocab_sz = len(word_indices)
    label_sz = len(label_indices)
    batch_size = 32

    X, y = input_fn(file_path, word_indices, label_indices)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = build_model(vocab_sz, len(label_indices))
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=1,
              validation_data=(x_test, y_test))

    y_pred = model.predict(x_test, batch_size=batch_size)
    y_pred = np.argmax(y_pred, axis=1)
    evaluate_f1(y_test, y_pred, label_indices)