#!/usr/bin/env python

import rospy
from spacetrack import SpaceTrackClient
import time
import schedule
import json


def tleSchedule():
	time.sleep(1)
	getTles()
	schedule.every().day.at("14:00").do(getTles)
	while True:
		print("hey")
		schedule.run_pending()
		time.sleep(60)

def testFunction():
	print("SEE ON TEST")

def getTles():
	catalog_numbers = []
	# for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/satellites.txt','r').readlines():
	# 	catalog_numbers.append(json.loads(line)['catalog_number'])
	for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/current_satellite.txt','r').readlines():
		catalog_numbers.append(int(line))
	print(catalog_numbers)
	st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
	print(st)
	tle = st.tle_latest(norad_cat_id=catalog_numbers, ordinal=1, format='3le').encode("utf-8")
	print(tle)
	print("PLS")
	formatTle(tle)

def formatTle(tle):
	tle_lines = tle.split('\n')[:-1]

	tles = [tle_lines[x:x+3] for x in xrange(0, len(tle_lines), 3)]

	tles_string = ""
	for i in tles:
		i[0] = i[0][2:len(i[0])]
		tles_string = tles_string + "{}\n{}\n{}\n".format(i[0], i[1], i[2])
		print(tles_string + "  TLE")

	print(tles_string)
	with open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tles.txt', 'w') as f:
		f.write(tles_string)

def main():
	tleSchedule()


if __name__ == '__main__':
	main()