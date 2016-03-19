#!/usr/bin/env python

"""
Data acquisition of the "Base Station"
	- Manages bluetooth connection and data retrieval
	- Performs a first pre-treatment to filter data and trigger first-response alarms
	- Records data for storage and asynchronous analysis
"""

__author__ = "Julien Beaudaux"
__copyright__ = "GNU v3"
__version__ = "0.1"
__email__ = "julienbeaudaux@gmail.com"



import bitalino
import time

import requests
import json
import sys

from termcolor import colored

colored

def ConnectBitalino(macAddress, batThresh=30, frequency=100):
	acqChannels = [2]
	digitalOutput = [0,0,0,0]

	global device
	device = bitalino.BITalino(macAddress)
	device.battery(batThresh)
	print colored("Connected to : %s"%(device.version()), "green")

	device.start(frequency, acqChannels)


def DisconnectBitalino():
	global device

	print colored("Disconnecting device", "red")

	if device is not None:
		device.stop()
		device.close()


def AcquireSamples(nSamples=1000):
	global device

	colored("Start samples acquisition", "green")

	samples = []
	i=0

	# Read samples
	while True:
		print device.read(nSamples)
		time.sleep(1)
		#print device.read(nSamples)[0][5]
		#for j in range(0,10):
		#	samples.append(device.read(nSamples)[j][5])

		#	format2json(samples, samples)




def format2json(listrate, listpodo):
	"""
	Formats lists of heart & podometry samples into Json format. Either write it to a file or POST it on server
	"""

	global dataFile
	global outputMode


	header = {'Content-Type': 'OpenHeart/json'}
	record = {'rate':listrate, 'podo':listpodo}

	values = [{"rate": k, "podo": v} for k, v in record.items()]
	formattedData = json.dumps(values, indent=4)

	print formattedData

	if outputMode == "file":
		dataFile.write(formattedData)
	elif outputMode == "post":
		res = requests.post('http://localhost/api/signal', data=formattedData, headers=header)
		print res


def mockupMode(extra, option=0):
	print "mockupMode"


def ecgMode(extra, option=0):
	global outputMode
	print colored("Output Mode : %s"%(outputMode), "yellow")

	try:
#		ConnectBitalino("20:15:10:26:65:41")
		ConnectBitalino("20:15:10:26:64:85")
		AcquireSamples()
		while True:
			pass
	except KeyboardInterrupt:
		DisconnectBitalino()
		sys.exit(0)


def simuMode(extra, option=0):
	print "simuMode"



def SimulatedData():
	i=0
	rate = []
	podo = []

	while True:
		# Create fake data and format it to JSON

		i = (i + 1) % 250
		rate.append(i)
		podo.append(250-i)

		if i%50 == 0:
			format2json(rate, podo)

			rate = []
			podo = []

			time.sleep(1)


# Provides details on the control center
def handleHelp(extra, option=0):
	print '\nOpenHeart base station'
	print '======================\n'
	print 'Commands'
	print '--------\n'
	print 'mockup\tIn this mode, pre-recorded or simulated data is used'
	print 'ecg\tConnects to the bitalino bracelet to collect data and use it'
	print 'simu\tCreate a data file of recorded data'
	print 'help\tEnters this very help menu'
	print ''

	sys.exit(0)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage: sudo python %s COMMAND OUTPUT [options]'%(sys.argv[0])
		sys.exit(-1)

	option = 0
	command_map = {'mockup': mockupMode, 'ecg': ecgMode, 'simu': simuMode, 'help': handleHelp}
	command = sys.argv[1]

	global outputMode 
	outputMode = sys.argv[2]

	if len(sys.argv) > 3:
		option = int(sys.argv[3])

	if command in command_map:
		command_map[command](sys.argv[2:], option)
	else:
		print 'Command not supported: {}'.format(command)
		sys.exit(-1)





	global dataFile
	dataFile = open("mockup.data", "w")

	try:
		SimulatedData()
	except :
		dataFile.close()
		print "Closed file mockup.data"
		sys.exit(0)
