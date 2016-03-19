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


if __name__ == '__main__':
	macAddress = "20:15:10:26:65:41"

	batteryThreshold = 30

	#Select the channels we want to retrieve and configure the device settings
	acqChannels = [0,3]
	samplingRate = 1000
	nSamples = 10
	digitalOutput = [0,0,1,1]


	device = bitalino.BITalino(macAddress)

	# Set battery threshold
	print device.battery(batteryThreshold)

	# Read BITalino version
	device.version()

	# Start Acquisition
	device.start(samplingRate, acqChannels)

	# Read samples
	print device.read(nSamples)

	# Turn BITalino led on
	device.trigger(digitalOutput)

	# Stop acquisition
	device.stop()

	# Close connection
	device.close()
