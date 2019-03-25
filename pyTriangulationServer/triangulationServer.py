import json
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold
import math

NUMBER_OF_POINTS = 6
'''
def find_coordinates(distanceMatrix):	
	#distanceMatrix /= np.amax(distanceMatrix)
	mds = manifold.MDS(n_components=2, dissimilarity='precomputed')
	results = mds.fit(distanceMatrix)
	coords = results.embedding_
	print (coords)
	plt.scatter(coords[:,0], coords[:,1], marker = 'o')
	labels =['node {0}'.format(i) for i in range(NUMBER_OF_POINTS)]
	print (distanceMatrix)
	for label, x, y in zip(labels, coords[:, 0], coords[:, 1]):
	    plt.annotate(
		label,
		xy=(x, y), xytext=(-20, 20),
		textcoords='offset points', ha='right', va='bottom',
		bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
		arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
	plt.show()
'''
def distance(coord1, coord2):
	return math.sqrt(math.pow(coord1[0] - coord2[0], 2) - math.pow(coord1[1] - coord2[1], 2))

def find_coordinates(distanceMatrix):
	coordinates = []
	#setting node0 to be at [0,0]
	coordinates.append([0,0])
	#setting node1 to be at [distance from node0, 0]
	coordinates.append([distanceMatrix[0][1],0])
	angle = math.acos((math.pow(distanceMatrix[0][1],2) + math.pow(distanceMatrix[0][2],2) - math.pow(distanceMatrix[1][2],2))/(2 * distanceMatrix[0][1]*distanceMatrix[0][2]))
	x = distanceMatrix[0][2] * math.cos(angle)
	y = distanceMatrix[0][2] * math.sin(angle)
	coordinates.append([x,y])
	for nodeToCalculate in range (3, NUMBER_OF_POINTS):
		angle = math.acos((math.pow(distanceMatrix[0][1],2) + math.pow(distanceMatrix[0][nodeToCalculate],2) - math.pow(distanceMatrix[1][nodeToCalculate],2))/(2 * distanceMatrix[0][1]*distanceMatrix[0][nodeToCalculate]))
		i = distanceMatrix[0][nodeToCalculate] * math.cos(angle)
		j = distanceMatrix[0][nodeToCalculate] * math.sin(angle)
		if(distance([i,j], coordinates[2]) != distanceMatrix[2][nodeToCalculate]):
			j=-j
		coordinates.append([i,j])
	print (coordinates)
	xArr = []
	yArr = []
	for data in coordinates:
		xArr.append(data[0])
		yArr.append(data[1])
	plt.scatter(xArr, yArr, marker = 'o')
	labels =['node {0}'.format(i) for i in range(NUMBER_OF_POINTS)]
	for label, x, y in zip(labels, xArr, yArr):
	    plt.annotate(
		label,
		xy=(x, y), xytext=(-20, 20),
		textcoords='offset points', ha='right', va='bottom',
		bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
		arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))
	plt.show()
	return

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



