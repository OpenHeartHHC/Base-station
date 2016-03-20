#!/usr/bin/env python

"""
Opens accelerometric data, plots and parse it
"""

from matplotlib import pyplot as plt
from matplotlib import animation

import numpy as np
from math import sqrt
import sys
import time

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 10000), ylim=(100, 300))
#ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))


# initialization function: plot the background of each frame
def init():
	line.set_data([], [])
	return line,

def update_line(num, data, line):
    line.set_data(ecg[..., :num])
    return line,

# animation function.  This is called sequentially
def animate(i):
	"""x = np.linspace(0, 2, 1000)
	y = np.sin(2 * np.pi * (x - 0.01 * i))

	print x, y
	time.sleep(5)

	line.set_data(x, y)
	return line,"""
	
	global axecg
	global ecg

	global tmpx
	global tmpy

	tmpx.append(axecg.pop())
	tmpy.append(ecg.pop())

	x = tmpy
	y = tmpx

	print x, y

	line.set_data(x, y)
	return line,



if __name__ == '__main__':
	infile = open(sys.argv[1], "r")

	global axecg
	global ecg

	global tmpx
	global tmpy

	tmpx = []
	tmpy = []

	ecg = []
	axecg = []
	
	i=0
	axe=0
	for myLine in infile:
		i+=1
		if i < 30000:
			ecg.append(float(myLine.replace('\n', '')))
			axecg.append(axe)
			axe = axe + 0.01

	infile.close()

	l, = plt.plot([], [], 'r-')

	# call the animator.  blit=True means only re-draw the parts that have changed.
	anim = animation.FuncAnimation(fig, update_line, fargs=(ecg, l), frames=200, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

"""if __name__ == '__main__':

	infile = open(sys.argv[1], "r")

	ecg = []
	axecg = []
	
	i=0
	axe=0
	for line in infile:
		i+=1
		if i < 300000:
			ecg.append(float(line.replace('\n', '')))
			axecg.append(axe)
			axe = axe + 0.01

	print axe

	infile.close()

	anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=True)

	#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

	plt.show()
"""