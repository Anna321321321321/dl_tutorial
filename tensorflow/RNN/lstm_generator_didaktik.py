from __future__ import absolute_import, division, print_function

import os
import pickle
from six.moves import urllib

import tflearn
from tflearn.data_utils import *

path = "zu05056.txt"

maxlen = 25

X, Y, char_idx = \
    textfile_to_semi_redundant_sequences(path, seq_maxlen=maxlen, redun_step=3)

g = tflearn.input_data([None, maxlen, len(char_idx)])
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                       learning_rate=0.001)

m = tflearn.SequenceGenerator(g, dictionary=char_idx,
                              seq_maxlen=maxlen,
                              clip_gradients=5.0,
                              checkpoint_path='model_didactic')

for i in range(10):
    seed = random_sequence_from_textfile(path, maxlen)
    print(m.generate(400, temperature=1.0, seq_seed=seed))
    m.fit(X, Y, validation_set=0.1, batch_size=128, n_epoch=1, run_id='shakespeare')
    print("-- TESTING --- epoch {}".format(i))
    print("-- Test with temperature of 1.0 --")
    print(m.generate(400, temperature=1.0, seq_seed=seed))
    print("-- Test with temperature of 0.5 --")
    print(m.generate(400, temperature=0.5, seq_seed=seed))