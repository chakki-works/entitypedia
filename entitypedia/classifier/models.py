from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM, Dropout


def build_model(vocab_sz, num_labels, emb_sz=128, dropout=0.2):
    model = Sequential()
    model.add(Embedding(vocab_sz, emb_sz, mask_zero=True))
    #model.add(Dropout(rate=dropout))
    model.add(LSTM(emb_sz, dropout=dropout, recurrent_dropout=dropout))
    #model.add(Dropout(rate=dropout))
    model.add(Dense(num_labels, activation='softmax'))

    return model
