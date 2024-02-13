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

def binary(num):
	return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))

mnist_digits = fetch_openml('mnist_784', version=1,parser='auto')
print(mnist_digits.keys())

x = mnist_digits["data"]
y = mnist_digits["target"]

x = x / 255.

sample_a = x.loc[[2]].to_numpy()
sample_b = x.loc[[25]].to_numpy()

print(sample_a)
print(sample_b)

sample_a_img = sample_a.reshape(28, 28)
sample_b_img = sample_b.reshape(28, 28)

plt.imshow(sample_a_img)
plt.show()
plt.imshow(sample_b_img)
plt.show()
 
file_path = "Binary_Digits.txt"
f = open(file_path, "w")
List_all_examples = []
image_amount = 20

for i in range(image_amount):
	sample = x.loc[[i]].to_numpy()
	transformed = [binary(float(element)) for element in sample[0]]
	label = y.loc[[i]].to_numpy()[0]
	print(transformed)
	print(y.loc[[i]].to_numpy()[0])
	List_all_examples.append([transformed,label])
	
f.write(str(List_all_examples))
f.close()
