import nltk
from nltk.stem.lancaster import lancasterStemmer
stemmer = lancasterStemmer()

import numpy
import tflearn
import tensoflow as tf
import random
import json
import pickle
 

with open("intents.json") as file:
	dat = json.load(file)

try:
	with open('data.pickle','rb') as f:
		words, labels, training, output = pickle.load(f)


except:
	words = []
	labels = []
	docs_x = []
	docs_y = []

	for intents in data['intents']:
		for pattern in intent['pattern']:
			wrd = nltk.word_tokenize(pattern)
			words.extend(wrds)
			docs_x.append(wrds)
			doc_y.append(intent['tag'])

		if intent['tag'] not in labels:
			labels.append(intent['tag'])

	words = [stemmer.stem(w.lower()) for w in words if w != '?']
	words = sorted(list(set(words)))

	labels = sorted(labels)

	training = []
	output = []

	out_empty = [0 for _ in range(len(labels))]

	for doc in enumerate(docs_x):
		bag = []
		wrds = [stemmer.ste(w) for w in doc]
		for w in words:
			if w in wrds:
				bag.append(1)
			else:
				bag.append(0)

		output_row = out_empty[:]
		output_row[labels.index(docs_y[x])] = 1

		training.append(bag)
		output.append(output_row)

	training = numpy.array(training)	
	output = np.array(output)

	
	with open('data.pickle','wb') as f:
		pickle.dump((words, labels, training, output), f)

tf.reset_default_graph()	

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
	model.load('mode.tflearn')
except:
	model.fit(training, output, n_epoch=1000, batch_size=8, show_metrix=True)
	model.save('model.tflearn')

def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[i] = (1)

	return numpy.array(bag)

def chat():
	print('Start the Chat(Type Quite to stop!)')
	while True:
		inp = input('You: ')
		if inp.lower() == 'Quite':
			break

		results = model.predict([bag_of_words(inp, words)])[0]
		results_index = numpy.argmax(results)
		tag = labels[results_index]

		if results[results_index] > 0.7:
			for tg in data['intents']:
				if tg['tag'] == tag:
					responses = tg[responses]
		print(random.choices(responses))
	else:
		print("I didn't get that, try again")

chat()		