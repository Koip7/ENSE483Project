'''
 *Justin Smith
 * ENSE483
 * Class Project
 * 
This file defines the triangulationServer
This server will read bluetooth RSII data from an MQTT server
It will then take that data to estimate the coordinates of the bluetooth nodes and will then plot them on a graph
 '''
import json
import paho.mqtt.client as mqtt
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold
import math
import traceback

#the number of points in the system, this value must at least be greater than 4
NUMBER_OF_POINTS = 10

"""
calculates the distance from coord1 to coord2
"""
def distance(coord1, coord2):
	return math.sqrt(math.pow(coord1[0] - coord2[0], 2) + math.pow(coord1[1] - coord2[1], 2))

"""
Given a matrix defining the distances between all nodes this function will plot the coordinates of each point only depending on the distance of node 0-2 to the rest of the nodes

The triangulation parts of this function is based on the alogorithm, describing the mathematical steps, located here:
https://stackoverflow.com/questions/10963054/finding-the-coordinates-of-points-from-distance-matrix
by Rasman
"""
def find_coordinates(distanceMatrix):
	coordinates = []
	#asignning the first point to be the origin
	coordinates.append([0,0])
	#asigning the second point and making it's X equal to the distance from the first point
	coordinates.append([distanceMatrix[0][1],0])
	print('initialized 1st and 2nd points')
	#detemining the angle
	try:
		var1 = math.pow(distanceMatrix[0][1],2) + math.pow(distanceMatrix[0][2],2) - math.pow(distanceMatrix[1][2],2)
		var2 = 2 * distanceMatrix[0][1]*distanceMatrix[0][2]
		var3 = var1/var2

		if var3 < -1:
			var3 = -1.0
		if var3 > 1:
			var3 = 1.0
		angle = math.acos(var3)
		#angle = math.acos((math.pow(distanceMatrix[0][1],2) + math.pow(distanceMatrix[0][2],2) - math.pow(distanceMatrix[1][2],2))/(2 * distanceMatrix[0][1]*distanceMatrix[0][2]))
		#finding the coordinates based on the angle of the third point
		x = distanceMatrix[0][2] * math.cos(angle)
		y = distanceMatrix[0][2] * math.sin(angle)
		coordinates.append([x,y])
		print('initialized 3rd point')
	except Exception as e:
		print(traceback.format_exc())
		print('could not initialize 3rd point')
	#Calculating the other coordinates
	for nodeToCalculate in range (3, NUMBER_OF_POINTS):
		try:
			#angle = math.acos((math.pow(distanceMatrix[0][1],2) + math.pow(distanceMatrix[0][nodeToCalculate],2) - math.pow(distanceMatrix[1][nodeToCalculate],2))/(2 * distanceMatrix[0][1]*distanceMatrix[0][nodeToCalculate]))
			var1 = math.pow(distanceMatrix[0][1],2) + math.pow(distanceMatrix[0][nodeToCalculate],2) - math.pow(distanceMatrix[1][nodeToCalculate],2)
			var2 = 2 * distanceMatrix[0][1]*distanceMatrix[0][nodeToCalculate]
			var3 = var1/var2

			if var3 < -1:
				var3 = -1.0
			if var3 > 1:
				var3 = 1.0
			angle = math.acos(var3)
			x = distanceMatrix[0][nodeToCalculate] * math.cos(angle)
			y = distanceMatrix[0][nodeToCalculate] * math.sin(angle)
			if(abs(distance([x,y], coordinates[2]) - distanceMatrix[2][nodeToCalculate]) > abs(distance([x,-y], coordinates[2]) - distanceMatrix[2][nodeToCalculate])):
				y=-y
			coordinates.append([x,y])
		except Exception as e:
			print(traceback.format_exc())
			print('could not initialized ' + str(nodeToCalculate) + ' point')
	print(coordinates)
	#Printing the coordinates in a graph
	graph_coordinates(coordinates)
	return

#Graphs coordinates
def graph_coordinates(coordinates):
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
		bbox=dict(boxstyle='round,pad=0.1', fc='yellow', alpha=0.5),
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
returns the distance calculated from RSSI
'''
def distance_from_RSSI(RSSI):
	MEASURED_POWER = -69
	N = 2
	return math.pow(10, (MEASURED_POWER - RSSI)/(10 * N))

'''
function stating what to do upon successfull message recived from a mqqt broker
'''
def on_message(client, userdata, msg):
	print('Recieved msg:'+ msg.topic + " " + str(msg.qos) + " "+ str(msg.payload))
	distanceMatrix = np.zeros((3,NUMBER_OF_POINTS))
	jsonMsg = str(msg.payload)	
	loadedJson = json.loads(jsonMsg)
	print('Done loading data')
	#setting values in the distance matrix
	for data in loadedJson["metrics"]:
		#convert RSSI to distance
		distanceMatrix[int(data[0])][int(data[1])] = distance_from_RSSI(float(loadedJson["metrics"][data]))
		print('in ' + data + ' storing ' + str(loadedJson["metrics"][data]) + ' calculated ' + str(distance_from_RSSI(float(loadedJson["metrics"][data]))) + ' stored in ' + str(int(data[0])) + ',' + str(int(data[1])))
	print('made distance matrix')
	print(distanceMatrix)
	find_coordinates(distanceMatrix)
	return


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("mqtt","")
client.connect("localhost", 1883)

client.loop_forever()


