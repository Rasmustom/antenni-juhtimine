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
import json
import re
from operator import itemgetter

passes = []
pub1 = ""
pub2 = ""
#control_msgs/JointControllerState


def tleSchedule():
	getTles()
	schedule.every().day.at("14:00").do(getTles)
	while True:
		schedule.run_pending()
		time.sleep(60)

def runProgram():
	global passes

	open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tles.txt', 'w').close()
	while True:
		print("No passes yet")
		if (os.stat('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tles.txt').st_size > 0):
			passes = getNextPasses([])
			break
		time.sleep(0.5)

	print(passes)
	startTime = passes[0][0][0]
	print(startTime)

	schedule.every(0.5).seconds.do(checkTime)
	while True:
		schedule.run_pending()
		time.sleep(0.5)

def checkTime():
	global passes
	if (len(passes[0]) > 0):
		satellite_time = ephem.localtime(passes[0][0][0]).strftime("%d-%m-%Y %H:%M:%S")
		current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		print(len(passes[0]))

		# print(passes[0].pop(0))
		print(current_time + "\n" + satellite_time + " " + passes[0][0][3])
		if (current_time == satellite_time):
			if (len(passes[0]) > 0):
				if (len(passes[0]) == 1) :
					last_set_time2 = ephem.localtime(passes[0][0][0]).strftime("%d-%m-%Y %H:%M:%S")
					print("AJA KONTROLL: ")
					print("LAST TIME: {}".format(last_set_time2))
					print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

				print(passes[0][len(passes[0]) - 1])
				pass_second = passes[0].pop(0);
				moveAntenna2(pass_second)
	else:
		# last_set_time = passes[0][len(passes[0])-1]
		# print("WTF ", passes)
		# print(last_set_time, last_set_time2)
		time.sleep(10)
		passes = getNextPasses(passes)
		# print(passes[0])
		# moveAntenna(passes[0])
		# moveAntennaOnce(passes[0][0][2], passes[0][0][1])

def moveAntenna2(move):
	global pub1
	global pub2
	print("AAAAAAAA {}".format(move))
	rospy.loginfo(move[2]-1.571)
	# for x in xrange(1,10):
	pub1.publish(move[2]-1.571)
	pub2.publish(move[1]-1.571)
	print("Miks sa ei publish")
	# rate = rospy.Rate(10)
	# while not rospy.is_shutdown():
	# 	connections1 = pub1.get_num_connections()
	# 	connections2 = pub2.get_num_connections()
	# 	rospy.loginfo("Connections: {}, {}".format(connections1, connections2))
	# 	if (connections1 > 0 and connections2 > 0):
	# 		print("IM CRYING")
	# 		pub1.publish(move[2]-1.571)
	# 		pub2.publish(move[1]-1.571)
	# 		break
	# 	print("WHYYY")
	# 	rate.sleep()

# def getTle():
# 	st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
# 	print(st)
# 	tle = st.tle_latest(norad_cat_id=42016, ordinal=1, format='3le').encode("utf-8")

# 	lines = tle.splitlines()
# 	lines[0] = lines[0][2:len(lines[0])]

# 	with open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tle.txt', 'w') as f:
# 		f.write("{}\n{}\n{}".format(lines[0], lines[1], lines[2]))

# 	print(tle)
# 	return lines
	
# def getNextPasses(passes):
# 	# satellite = ephem.readtle("ESTCUBE 1", 
# 	# 	"1 39161U 13021C   18084.14857487  .00000203  00000-0  40243-4 0  9994",
# 	# 	"2 39161  98.0082 171.2809 0008559 335.3503  24.7303 14.72036145262086")

# 	lines = []
# 	for line in open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tle.txt','r').readlines():
# 		lines.append(line)

# 	satellite = ephem.readtle(lines[0], lines[1], lines[2])

# 	obs = ephem.Observer()
# 	obs.lat = '59.394870'
# 	obs.long = '24.661399'
# 	passes = []

# 	for i in range(3):
# 		pass_parts = []
# 		rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
# 		print(rise_time, set_time)
# 		while rise_time < set_time:
# 			obs.date = rise_time
# 			satellite.compute(obs)
# 			pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az))))
# 			print("%s | %4.1f %5.1f | %4.1f %+6.1f | %5.1f" % \
# 				(rise_time,
# 					math.degrees(satellite.alt),
# 					math.degrees(satellite.az),
# 					math.degrees(satellite.sublat),
# 					math.degrees(satellite.sublong),
# 					satellite.elevation/1000.))
# 			rise_time = ephem.Date(rise_time + ephem.second)
# 		passes.append(pass_parts)
# 		obs.date = rise_time + ephem.minute
# 	print(passes)
# 	return passes

def moveAntenna(passes):
	starttime = time.time()
	pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
	pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)

	for i in passes:
		# rospy.Subscriber("/antenna/joint1_position_controller/state", JointControllerState, smth)
		print(i)
		pub1.publish(i[2]-1.571)
		pub2.publish(i[1]-1.571)
		time.sleep(0.1 - ((time.time() - starttime) % 0.1))

def moveAntennaOnce(az, alt):
	pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
	pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)
	print(az, alt)
	print(pub1, pub2)
	for x in range(2):
		pub1.publish(az-1.571)
		pub2.publish(alt-1.571)
		# az = az + 0.1
		# alt = alt + 0.1
		time.sleep(1)


def addSatelliteToTrack(catalog_number, name):
	lines = []
	sat_exists = False
	for line in open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/satellites.txt','r').readlines():
		lines.append(json.loads(line))
	for i in lines:
		if i['catalog_number'] == catalog_number:
			sat_exists = True
			break
	if not sat_exists:
		dict = {'name': name, 'catalog_number': catalog_number}
		with open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/satellites.txt', 'a') as f:
			f.write("{}\n".format(json.dumps(dict)))

def getTles():
	catalog_numbers = []
	for line in open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/satellites.txt','r').readlines():
		catalog_numbers.append(json.loads(line)['catalog_number'])
	print(catalog_numbers)
	st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
	print(st)
	tle = st.tle_latest(norad_cat_id=catalog_numbers, ordinal=1, format='3le').encode("utf-8")
	print(tle)
	tle_lines = tle.split('\n')[:-1]

	tles = [tle_lines[x:x+3] for x in xrange(0, len(tle_lines), 3)]

	tles_string = ""
	for i in tles:
		i[0] = i[0][2:len(i[0])]
		tles_string = tles_string + "{}\n{}\n{}\n".format(i[0], i[1], i[2])
		# with open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tles.txt', 'a') as f:
		# 	f.write("{}\n{}\n{}\n".format(i[0], i[1], i[2]))
	# print(tles)
	with open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tles.txt', 'w') as f:
		f.write(tles_string)

def getNextPasses(passes):
	# satellite = ephem.readtle("ESTCUBE 1", 
	# 	"1 39161U 13021C   18084.14857487  .00000203  00000-0  40243-4 0  9994",
	# 	"2 39161  98.0082 171.2809 0008559 335.3503  24.7303 14.72036145262086")

	lines = []
	for line in open('/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tles.txt','r').readlines():
		lines.append(line)

	tles = [lines[x:x+3] for x in xrange(0, len(lines), 3)]
	print(tles)

	all_passes = []
	for x in tles:
		obs = ephem.Observer()
		obs.lat = '59.394870'
		obs.long = '24.661399'
		satellite = ephem.readtle(x[0], x[1], x[2])

		# satellite = ephem.readtle(lines[0], lines[1], lines[2])

		passes = []

		for i in range(3):
			pass_parts = []
			rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
			print(rise_time, set_time, x[0])
			satellite_time = ephem.localtime(rise_time)
			current_time = datetime.now()
			print(satellite_time < current_time)
			print(satellite_time > current_time)
			if rise_time > set_time:
				obs.date = set_time + ephem.minute
				print("ASDASDASDASD")
				continue
			while rise_time < set_time:
				obs.date = rise_time
				satellite.compute(obs)
				pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az)), x[0]))
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
		all_passes.extend(passes)
		# print("PASSES: {} ".format(all_passes))
	print("ALL PASSES LENGTH: {}".format(len(all_passes)))
	for x in all_passes:
		if len(x) > 0:
			print(x[0])
	# print("{}\n{}\n{}".format(all_passes[0][0], all_passes[1][0], all_passes[2][0]))
	all_passes.sort(key=itemgetter(0, 0))
	# all_passes.sort(key=lambda tup:tup[0][0])

	all_passes = all_passes[0:3]
	for x in all_passes:
		print(x[0])


	return all_passes

def main():
	
	global pub1
	global pub2
	pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
	pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)

	rospy.init_node('control_monitor', anonymous=True)
	# rospy.Subscriber("/antenna/joint1_position_co xzntroller/state", JointControllerState, smth)

	# st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
	# print(st)
	# tle = st.tle_latest(norad_cat_id=39161, ordinal=1, format='3le').encode("utf-8")

	# print getTle()
	# passes = []
	# passes = getNextPasses(passes)
	# # # passes = getNextPasses(passes)
	# # print(passes[0][0][1])
	# print passes


	# starttime = time.time()
	# pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
	# pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)

	# # rospy.Subscriber("/antenna/joint1_position_controller/state", JointControllerState, smth)
	# for i in passes:
	# 	pub1.publish(0)
	# 	pub2.publish(0)

	# print(len(passes[0]))

	# moveAntenna(passes[3])
	# moveAntennaOnce(passes[1][0][1],passes[1][0][2])

	addSatelliteToTrack(39161, "ESTCUBE 1")
	addSatelliteToTrack(41850, "CELTEE 1")
	addSatelliteToTrack(41789, "ALSAT 1N")
	addSatelliteToTrack(42016, "AL-FARABI 1")
	addSatelliteToTrack(43043, "AEROCUBE 7C")
	addSatelliteToTrack(25544, "ISS")
	addSatelliteToTrack(42775, "AALTO-1")
	addSatelliteToTrack(41852, "AEROCUBE 8D")
	addSatelliteToTrack(43020, "ASTERIA")
	addSatelliteToTrack(40034, "ANTELSAT")

	pub1.publish(0)
	pub2.publish(0)

	# getTles()
	# getNextPasses([])

	# print(re.match('^((?:[^\n]*\n){%d}[^\n]*)\n(.*)' % (3-1), tle).groups())

	# for i in re.findall('^((.+?\n){3})(.+)', tle):
		# print(i.split("\n"))
	# p = multiprocessing.Process(target=tleSchedule)
	# p.start()

	# d = multiprocessing.Process(target=runProgram)
	# d.start()


	# rospy.spin()


if __name__ == '__main__':
	main()

