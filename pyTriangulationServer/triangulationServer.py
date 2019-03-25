import json
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold

NUMBER_OF_POINTS = 6

def find_coordinates(distanceMatrix):	
	distanceMatrix /= np.amaz(distanceMatrix)
	mds = manifold.MDS(n_components=2, dissimilarity='precomputed')
	results = mds.fit(distanceMatrix)
	coords = results.embedding_
	print (coords)
	plt.scatter(coords[:,0], coords[:,1], marker = 'o')
	plt.show()
	
	

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe("kura/kura_client/RSSI/data")

def on_message(client, userdata, msg):
	print('Recieved msg:'+ msg.topic + " " + str(msg.qos) + " "+ str(msg.payload))
	distanceMatrix = np.zeros((NUMBER_OF_POINTS,NUMBER_OF_POINTS))
	jsonMsg = str(msg.payload)	
	loadedJson = json.loads(jsonMsg)
	print('Done loading file')
	for data in loadedJson["metrics"]:
		distanceMatrix[int(data[0])][int(data[1])] = loadedJson["metrics"][data]
		distanceMatrix[int(data[1])][int(data[0])] = loadedJson["metrics"][data]
	print('made distance matrix')
	find_coordinates(distanceMatrix)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("mqtt","")
client.connect("localhost", 1883)

client.loop_forever()



