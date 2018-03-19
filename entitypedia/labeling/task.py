import os
import itertools

import numpy as np
from gensim.corpora.dictionary import Dictionary
from gensim.models.keyedvectors import KeyedVectors
from sklearn.linear_model import SGDClassifier
from seqeval.metrics import f1_score, classification_report

from entitypedia.labeling.loader import load


def batch_iter(data, labels, batch_size=32, shuffle=True, preprocess=None):
    num_batches_per_epoch = int((len(data[0]) - 1) / batch_size) + 1

    def data_generator():
        """
        Generates a batch iterator for a dataset.
        """
        data_size = len(data[0])
        while True:
            indices = np.arange(data_size)
            # Shuffle the data at each epoch
            if shuffle:
                indices = np.random.permutation(indices)

            for batch_num in range(num_batches_per_epoch):
                start_index = batch_num * batch_size
                end_index = min((batch_num + 1) * batch_size, data_size)
                X = [d[indices[start_index: end_index]] for d in data]
                y = labels[indices[start_index: end_index]]
                yield preprocess(X, y)

    return num_batches_per_epoch, data_generator()


if __name__ == '__main__':
    # Load
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    train_file = os.path.join(DATA_DIR, 'conll.txt')
    embedding_file = os.path.join(DATA_DIR, 'word2vec.gensim.model')
    model = KeyedVectors.load(embedding_file)
    words, poses, labels = load(train_file)
    data = np.asarray([words, poses])
    labels = np.asarray(labels)

    # preprocess
    word_dic = Dictionary(words)
    pos_dic = Dictionary(poses)
    label_dic = Dictionary(labels)
    unk_vec = np.zeros(shape=(50,))

    def preprocess(X, y):
        embeddings = [[model[w] if w in model else unk_vec for w in sent] for sent in X[0]]
        window_size = 3
        inputs = []
        outputs = []
        for sent, labels in zip(embeddings, y):
            for i in range(len(sent)):
                vec = sent[max(i-window_size, 0):i+window_size+1]
                label = labels[i]
                feature_label = labels[max(i-window_size, 0): i]
                if i < window_size:
                    vec = [unk_vec for _ in range(window_size-i)] + vec
                    label = 'O'
                    feature_label = ['O' for _ in range(window_size - i)] + feature_label
                if i >= len(sent) - window_size:
                    vec = vec + [unk_vec for _ in range(i-(len(sent)-window_size-1))]
                    label = 'O'
                assert len(feature_label) == window_size
                fl = np.zeros((len(label_dic)*window_size,))
                for i, num in enumerate(label_dic.doc2idx(feature_label)):
                    fl[(i+1)*num] = 1
                inp = np.concatenate(vec)
                inp = np.concatenate((inp, fl))
                # assert inp.shape == (250, )
                # print(feature_label)
                # assert len(feature_label) == window_size

                inputs.append(inp)
                outputs.append(label)

        return inputs, outputs

    num_steps, generator = batch_iter(data, labels, preprocess=preprocess)

    classes = np.unique(list(itertools.chain(*labels)))
    clf = SGDClassifier()
    n_iter = 5
    for n in range(n_iter):
        print('n_iter: {}'.format(n + 1))
        for _ in range(num_steps):
            print('  steps: {}'.format(_))
            X_train, y_train = generator.__next__()
            clf.partial_fit(X_train, y_train, classes=classes)

    y_pred = clf.predict(X_train)
    print(f1_score([list(y_train)], [list(y_pred)]))
    print(classification_report([list(y_train)], [list(y_pred)]))