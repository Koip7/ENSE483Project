'''
 *Justin Smith
 * ENSE483
 * Class Project
 * 
 * This file defines the triangulationServer
This server will read bluetooth RSII data from an MQTT server
It will then take that data to estimate the coordinates of the bluetooth nodes and will then plot them on a graph
 '''


import json
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold
import math

#the number of points in the system, this value must at least be greater than 4
NUMBER_OF_POINTS = 6

"""
calculates the distance from coord1 to coord2
"""
def distance(coord1, coord2):
	return math.sqrt(math.pow(coord1[0] - coord2[0], 2) - math.pow(coord1[1] - coord2[1], 2))

"""
Given a matrix defining the distances between all nodes this function will plot the coordinates of each point only depending on the distance of node 0-2 to the rest of the nodes

The triangulation parts of this function is based on the alogorithm, describing the mathematical steps, located here:
https://stackoverflow.com/questions/10963054/finding-the-coordinates-of-points-from-distance-matrix
by Rasman
The 'Steps' stated correspond to the defined mathematical equations described in the post above

"""
def find_coordinates(distanceMatrix):
	coordinates = []
	#Step 1, arbitrarily assign one point P1 as (0,0).
	coordinates.append([0,0])
	#Step 2, arbitrarily assign one point P2 along the positive x axis. (0, Dp1p2)
	coordinates.append([distanceMatrix[0][1],0])
	#Use the cosine law to determine the distance:
	angle = math.acos((math.pow(distanceMatrix[0][1],2) + math.pow(distanceMatrix[0][2],2) - math.pow(distanceMatrix[1][2],2))/(2 * distanceMatrix[0][1]*distanceMatrix[0][2]))
	x = distanceMatrix[0][2] * math.cos(angle)
	y = distanceMatrix[0][2] * math.sin(angle)
	coordinates.append([x,y])
	#Step 4: To determine all the other points, repeat step 3, to give you a tentative y coordinate. (Xn, Yn).
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

'''
function stating what to do upon successfull connection to a mqqt broker
'''
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	#the subscription
	client.subscribe("kura/kura_client/RSSI/data")
	return

'''
function stating what to do upon successfull message recived from a mqqt broker
'''
def on_message(client, userdata, msg):
	print('Recieved msg:'+ msg.topic + " " + str(msg.qos) + " "+ str(msg.payload))
	distanceMatrix = np.zeros((NUMBER_OF_POINTS,NUMBER_OF_POINTS))
	jsonMsg = str(msg.payload)	
	loadedJson = json.loads(jsonMsg)
	print('Done loading file')
	#setting values in the distance matrix
	for data in loadedJson["metrics"]:
		distanceMatrix[int(data[0])][int(data[1])] = loadedJson["metrics"][data]
		distanceMatrix[int(data[1])][int(data[0])] = loadedJson["metrics"][data]
	print('made distance matrix')
	
	find_coordinates(distanceMatrix)
	return


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("mqtt","")
client.connect("localhost", 1883)

client.loop_forever()



