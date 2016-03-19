#!/usr/bin/env python

"""
Opens accelerometric data, parse it
"""

from math import sqrt
import sys

def stepper(x, y, z):
	final = []
	average = []

	for i in range(len(x)):
		final.append(sqrt(xval[i]**2 + yval[i]**2 + zval[i]**2))


	average = 0
	for item in final:
		average += item
	average = average/len(final)

	steps = 0
	belowed = False
	thresh = 50
	for index in range(len(final)):
		if final[index] > average and belowed > thresh:
			steps += 1
			belowed = 0
		elif final[index] < average:
			belowed += 1

	print "Number of steps : %d"%(steps)


if __name__ == '__main__':
	print sys.argv[1]

	infile = open(sys.argv[1], "r")

	xval = []
	yval = []
	zval = []
	i=0

	linesPerAxis = 6000

	for line in infile:
		line=line.replace('\n', '')
		if i < linesPerAxis:
			xval.append(float(line)-50)
		elif i < linesPerAxis * 2:
			yval.append(float(line))
		else:
			zval.append(float(line)+20)

		i = i+1

	xtmp = []
	ytmp = []
	ztmp = []

	for j in range(len(xval)):
		xtmp.append(xval[j])
		if j%1000 == 0 and j!=0:
			stepper(xtmp, ytmp, ztmp)
			xtmp = []
			ytmp = []
			ztmp = []