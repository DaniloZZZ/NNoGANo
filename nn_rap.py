# -*- coding: utf-8 -*-
from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, GRU
from keras.optimizers import Adam, RMSprop
from keras.models import load_model
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io
import urllib as r
import bs4
from nltk import word_tokenize, pos_tag
import numpy as np


def load_lstm():
    model = load_model(u'lstm-rap-model-50-epochs')
    return model

lstm = load_lstm()

with open('chars.pkl', 'r') as f:
    chars = pickle.load(f)


with open('char_indices.pkl', 'r') as f:
    char_indices = pickle.load(f)

with open('indices_char.pkl', 'r') as f:
    indices_char = pickle.load(f)


def get_new_word(history=u'', model=lstm):
    diversity = 0.2
    if len(history) < len(u"хое станека припев ты сам залетаю на trape припев><"):
        history = u'хое станека припев ты сам залетаю на trape припев><'
        
    sentence = history[-maxlen:]
    generated = ""
    generated += sentence
    output = []
    new_words = 0
    for i in range(400):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, diversity)
        next_char = indices_char[next_index]

        generated += next_char
        if next_char not in ['<', '>', '']:
            output.append(next_char[0])
            if next_char == ' ':
                if len(output) > 0:
                    new_words += 1
        
        sentence = sentence[1:] + next_char

        if new_words >= 10:
            return "".join(output).split()
        
    return ["", "", ""]
    