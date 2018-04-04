#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from control_msgs.msg import JointControllerState
from spacetrack import SpaceTrackClient
from pyorbital import tlefile
from pyorbital.orbital import Orbital
from datetime import datetime
import sys
import math
import ephem
import sched, time
import schedule
import multiprocessing
import os

passes = []

#control_msgs/JointControllerState


def getTle():
	st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
	tle = st.tle_latest(norad_cat_id=39161, ordinal=1, format='3le').encode("utf-8")

	lines = tle.splitlines()
	lines[0] = lines[0][2:len(lines[0])]

	with open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tle.txt', 'w') as f:
		f.write("{}\n{}\n{}".format(lines[0], lines[1], lines[2]))

	print(tle)
	return lines
	
def getNextPasses(passes):
	# satellite = ephem.readtle("ESTCUBE 1", 
	# 	"1 39161U 13021C   18084.14857487  .00000203  00000-0  40243-4 0  9994",
	# 	"2 39161  98.0082 171.2809 0008559 335.3503  24.7303 14.72036145262086")
	getTle()

	open('/home/rasmus/catkin_ws/src/antenna_controller/scripts/next_passes.txt', 'w').close()
	with open('/home/rasmus/catkin_ws/src/antenna_controller/scripts/next_passes.txt', 'a') as f:
		f.write("{}\n".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))


	lines = []
	for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tle.txt','r').readlines():
		lines.append(line)

	satellite = ephem.readtle(lines[0], lines[1], lines[2])

	obs = ephem.Observer()
	obs.lat = '59.394870'
	obs.long = '24.661399'
	passes = []

	for i in range(10):
		pass_parts = []
		rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
		start_time = rise_time
		max_az = 0
		# print(rise_time, math.degrees(rise_az), max_alt_time, math.degrees(max_alt), set_time, math.degrees(set_az))
		while rise_time < set_time:
			obs.date = rise_time
			satellite.compute(obs)
			pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az))))
			# print(rise_time, max_alt_time)
			if str(rise_time) == str(max_alt_time):
				max_az = math.degrees(satellite.az)
				# print(math.degrees(satellite.az))
			# print("%s | %4.1f %5.1f | %4.1f %+6.1f | %5.1f" % \
			# 	(rise_time,
			# 		math.degrees(satellite.alt),
			# 		math.degrees(satellite.az),
			# 		math.degrees(satellite.sublat),
			# 		math.degrees(satellite.sublong),
			# 		satellite.elevation/1000.))
			rise_time = ephem.Date(rise_time + ephem.second)
		passes.append(pass_parts)
		obs.date = rise_time + ephem.minute
		print("{} - Rise az: {} \n{} - Max az: {}, Maz alt: {} \n{} - Set az: {} \n".format(start_time, math.degrees(rise_az), max_alt_time, max_az, math.degrees(max_alt), set_time, math.degrees(set_az)))

		with open('/home/rasmus/catkin_ws/src/antenna_controller/scripts/next_passes.txt', 'a') as f:
			f.write("{} - Rise az: {} \n{} - Max az: {}, Maz alt: {} \n{} - Set az: {} \n".format(start_time, math.degrees(rise_az), max_alt_time, max_az, math.degrees(max_alt), set_time, math.degrees(set_az)))

	# print(passes)
	return passes


def main():
	getNextPasses([])


if __name__ == '__main__':
	main()