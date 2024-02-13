import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn import metrics as ms
from sklearn.datasets import fetch_openml
import pickle
import pandas
import struct

mnist_digits = fetch_openml('mnist_784', version=1,parser='auto')
x = mnist_digits["data"]
y = mnist_digits["target"]


x_train, x_test = x[:60000], x[60000:]
y_train, y_test = y[:60000], y[60000:]

mlp = MLPClassifier(hidden_layer_sizes=(15, ), max_iter=10, alpha=1e-4, activation = "logistic",
             	solver='sgd', verbose=10, random_state=1, learning_rate_init=.1)

x = x / 255.

mlp.out_activation_ = "softmax"

mlp.fit(x_train, y_train)

f1,f2 = open("weights.txt", "w"), open("biases.txt", "w")

for layers in mlp.coefs_:
	for neurons in layers:
   	f1.write(str(neurons)+"\n")
f1.close()

for layers in mlp.intercepts_:
	for neurons in layers:
   	f2.write(str(neurons)+"\n")
f2.close()



