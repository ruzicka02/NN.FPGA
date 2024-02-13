import struct
import os

def binary(num):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', num))

def create_folder(path):
	try:
		os.makedirs(path)
		print("Folder "+str(path)+" created")
	except FileExistsError:
	    print("Folder "+str(path)+" already there") 


network = [784,15,10]
file = open("weights.txt","r")

weights = file.read()
weights_list = weights.replace("\n","").replace("[","").split("]")

Partitioned_list = [element.split() for element in weights_list[:-1] ]

Layered_list = [[Partitioned_list[i] for i in range(sum(network[:c]),sum(network[:c+1])) ] for c in range(len(network)-1)]

regrouped = [[[binary(float(Layered_list[c][x][i])) for x in range(network[c])] for i in range(network[c+1])] for c in range(len(network)-1)]

file.close()


file = open("biases.txt","r")

biases = file.read()
biases_list = biases.split("\n")[:-1]

transformed_biases = [[binary(float(biases_list[i])) for i in range(sum(network[1:c]),sum(network[1:c+1]))	] for c in range(1,len(network))]

file.close()


path = "./NeuralNetwork"

create_folder(path)
create_folder(path+"/Weights_folder")
create_folder(path+"/Biases_folder")

for layer_nr in range(len(regrouped)):
	f = open(path+"/Weights_folder"+"/Weights_"+str(layer_nr)+".mem", "w")
	for neuron in regrouped[layer_nr]:
		for weight in neuron:
			f.write(str(weight)+"\n")

for layer_nr in range(len(transformed_biases)):
	f = open(path+"/Biases_folder"+"/Biases_"+str(layer_nr)+".mem", "w")
	for bias in transformed_biases[layer_nr]:
		f.write(str(bias)+"\n")


# This creates the following folder/file - structure:
#
# NeuralNetwork
# ├── Weights_folder
# │   ├── Weights_1
# │   ├── Weights_2
# │   └── ...
# └── Biases_folder
#     ├── Biases_1
#     ├── Biases_2
#     └── ...
