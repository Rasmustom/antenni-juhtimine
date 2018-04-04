#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from control_msgs.msg import JointControllerState
from spacetrack import SpaceTrackClient
from datetime import datetime
from operator import itemgetter
import math
import ephem
import time
import schedule
import multiprocessing
import os
import json
import re

passes = []
pub1 = ""
pub2 = ""
#control_msgs/JointControllerState

def runProgram():
	open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tles.txt', 'w').close()
	global passes
	global pub1, pub2
	pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
	pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)
	rospy.init_node('control_monitor', anonymous=True)

	while True:
		print("No passes yet")
		if (os.stat('/home/rasmus/catkin_ws/src/antenna_controller/tle/tles.txt').st_size > 0):
			passes = getNextPasses([])
			break
		time.sleep(0.5)

	print(passes)
	startTime = passes[0][0][0]
	moveAntenna(passes[0][0])
	print(startTime)

	schedule.every(0.5).seconds.do(checkTime)
	while True:
		schedule.run_pending()
		time.sleep(0.5)

def checkTime():
	global passes

	if (len(passes[0]) > 0):
		for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/current_satellite.txt','r').readlines():
			if not (int(line) == passes[0][0][4]):
				print("SAT HAS CHANGED {}, {}".format(line, passes[0][0][4]))
				passes = getNextPasses(passes)
				moveAntenna(passes[0][0])
			break
		satellite_time = ephem.localtime(passes[0][0][0])
		current_time = datetime.now()
		satellite_time_string = satellite_time.strftime("%d-%m-%Y %H:%M:%S")
		current_time_string = current_time.strftime("%d-%m-%Y %H:%M:%S")
		print(len(passes[0]))

		print(current_time_string + "\n" + satellite_time_string + " " + passes[0][0][3])
		if (current_time_string == satellite_time_string):
			if (len(passes[0]) > 0):
				if (len(passes[0]) == 1) :
					last_set_time2 = ephem.localtime(passes[0][0][0]).strftime("%d-%m-%Y %H:%M:%S")
					print("AJA KONTROLL: ")
					print("LAST TIME: {}".format(last_set_time2))
					print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

				print(passes[0][len(passes[0]) - 1])
				pass_second = passes[0].pop(0);
				moveAntenna(pass_second)
		elif (current_time > satellite_time):
			passes = getNextPasses(passes)

	else:
		time.sleep(10)
		passes = getNextPasses(passes)
		moveAntenna(passes[0][0])

def moveAntenna(move):
	global pub1, pub2

	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		connections1 = pub1.get_num_connections()
		connections2 = pub2.get_num_connections()
		rospy.loginfo("Connections: {}, {}".format(connections1, connections2))
		if (connections1 > 0 and connections2 > 0):
			pub1.publish(move[2]-1.571)
			pub2.publish(move[1]-1.571)
			break
		rate.sleep()
		# time.sleep(0.1)
	print("DONE")


def addSatelliteToTrack(catalog_number, name):
	lines = []
	sat_exists = False
	for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/satellites.txt','r').readlines():
		lines.append(json.loads(line))
	for i in lines:
		if i['catalog_number'] == catalog_number:
			sat_exists = True
			break
	if not sat_exists:
		dict = {'name': name, 'catalog_number': catalog_number}
		with open('/home/rasmus/catkin_ws/src/antenna_controller/tle/satellites.txt', 'a') as f:
			f.write("{}\n".format(json.dumps(dict)))

def getNextPasses(passes):
	lines = []
	for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tles.txt','r').readlines():
		lines.append(line)

	tles = [lines[x:x+3] for x in xrange(0, len(lines), 3)]
	print(tles)

	all_passes = []
	for x in tles:
		obs = ephem.Observer()
		obs.lat = '59.394870'
		obs.long = '24.661399'
		obs.horizon = '10'
		print(x)
		satellite = ephem.readtle(x[0], x[1], x[2])
		satellite.compute(obs)

		# satellite = ephem.readtle(lines[0], lines[1], lines[2])

		passes = []

		for i in range(3):
			pass_parts = []
			rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
			print(rise_time, set_time, x[0])
			satellite_time = ephem.localtime(rise_time)
			current_time = datetime.now()
			if rise_time > set_time:
				obs.date = set_time + ephem.minute
				print("ASDASDASDASD")
				continue
			while rise_time < set_time:
				obs.date = rise_time
				satellite.compute(obs)
				pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az)), x[0], int(x[2].split(" ")[1])))
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

def subscribe():
	rospy.init_node('control_monitor', anonymous=True)

	rospy.Subscriber("/antenna/joint1_position_controller/state", JointControllerState, smth)
	rospy.Subscriber("/antenna/joint2_position_controller/state", JointControllerState, smth)
	time.sleep(0.5)
	rospy.spin()
	
def smth(data):
	rospy.loginfo("DATA: %s", data.set_point)


def main():

	# # rospy.Subscriber("/antenna/joint1_position_controller/state", JointControllerState, smth)

	addSatelliteToTrack(39161, "ESTCUBE 1")
	# addSatelliteToTrack(41850, "CELTEE 1")
	# addSatelliteToTrack(41789, "ALSAT 1N")
	# addSatelliteToTrack(42016, "AL-FARABI 1")
	# addSatelliteToTrack(43043, "AEROCUBE 7C")
	# addSatelliteToTrack(25544, "ISS")
	# addSatelliteToTrack(42775, "AALTO-1")
	# addSatelliteToTrack(41852, "AEROCUBE 8D")
	# addSatelliteToTrack(43020, "ASTERIA")
	# addSatelliteToTrack(40034, "ANTELSAT")
	# addSatelliteToTrack(32787, "COMPASS-1")
	# addSatelliteToTrack(42785, "DIAMOND GREEN")
	# addSatelliteToTrack(39153, "CUBEBUG-1")
	# addSatelliteToTrack(42793, "CICERO 6")
	# addSatelliteToTrack(42724, "DUTHSAT")
	# addSatelliteToTrack(32788, "AUUSAT-1")
	# addSatelliteToTrack(32789, "DELFI-C3")

	# curr = 0
	# for x in xrange(1,100):
	# 	rate = rospy.Rate(10)
	# 	pub1_done = False
	# 	pub2_done = False
	# 	while not rospy.is_shutdown():
	# 		connections1 = pub1.get_num_connections()
	# 		connections2 = pub2.get_num_connections()
	# 		rospy.loginfo("Connections: {}, {}".format(connections1, connections2))
	# 		if (connections1 > 0):
	# 			pub1_done = True
	# 			pub1.publish(curr)
	# 			if pub2_done:
	# 				break
	# 		if (connections2 > 0):
	# 			pub2_done = True
	# 			pub2.publish(curr)
	# 			if pub1_done:
	# 				break
	# 		rate.sleep()
	# 	print("DONE")
	# 	curr = curr + 0.1
	# 	time.sleep(0.1)

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

	# getTles()
	# getNextPasses([])

	# print(re.match('^((?:[^\n]*\n){%d}[^\n]*)\n(.*)' % (3-1), tle).groups())

	# for i in re.findall('^((.+?\n){3})(.+)', tle):
		# print(i.split("\n"))

	# subscribe()

	runProgram()

	# p = multiprocessing.Process(target=tleSchedule)
	# p.start()

	# d = multiprocessing.Process(target=runProgram)
	# d.start()

	# sad = multiprocessing.Process(target=subscribe)
	# sad.start()

	#Kui anda ette satelliit, mis vaatev'lja kunagi ei joua, siis error  + 
	#Sujuv liikumine. URDF korda
	#Min horizon - Vist tootab, aga kontrolli ule. Lisaks vaja kontrollida satelliitide ulelennu ajad. Tundub, et horizoni panemisega annabki ta ulelennu vastavast horizonis horizonini. Meie tahame, et ta lihtsalt skipiks need, mis ule mingi horizoni kunagi ei joua, aga hakkaks neid jalgima ikkagi nullist. For, if
	#Kui gazebo ei toota


	# rospy.spin()


if __name__ == '__main__':
	main()

