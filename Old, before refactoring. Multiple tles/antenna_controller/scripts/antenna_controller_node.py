#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
from std_msgs.msg import String
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

#control_msgs/JointControllerState

class AntennaController():
	"""docstring for AntennaController"""
	def __init__(self):
		# super(AntennaController, self).__init__()
		self.passes = []
		self.pub1 = ""
		self.pub2 = ""
		self.last_move_direction = 0
		self.is_stopped = False
		self.local = time.time()

	def runProgram(self):
		open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tles.txt', 'w').close()
		self.pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
		self.pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)
		rospy.init_node('control_monitor', anonymous=True)

		while not (os.stat('/home/rasmus/catkin_ws/src/antenna_controller/tle/tles.txt').st_size > 0):
			print("No tle yet")
			time.sleep(0.5)

		self.getNextPasses()
		self.moveAntennaOnce(self.passes[0][0])

		# print(self.passes)

		schedule.every(0.5).seconds.do(self.checkTime)
		while True:
			schedule.run_pending()
			time.sleep(0.5)

	def testFunction(self):
		print("CHECK FOR SECONDS: {}".format(time.time() - self.local))

	def checkTime(self):
		if (len(self.passes[0]) > 0):
			for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/current_satellite.txt','r').readlines():
				if not (int(line) == self.passes[0][0][4]):
					print("SAT HAS CHANGED {}, {}".format(line, self.passes[0][0][4]))
					self.getNextPasses()
					self.moveAntennaOnce(self.passes[0][0])
				break
			satellite_time = ephem.localtime(self.passes[0][0][0])
			current_time = datetime.now()
			satellite_time_string = satellite_time.strftime("%d-%m-%Y %H:%M:%S")
			current_time_string = current_time.strftime("%d-%m-%Y %H:%M:%S")
			print(len(self.passes[0]))

			print(current_time_string + "\n" + satellite_time_string + " " + self.passes[0][0][3])
			if (current_time_string == satellite_time_string):
				if (len(self.passes[0]) > 0):
					if (len(self.passes[0]) == 1) :
						last_set_time2 = ephem.localtime(self.passes[0][0][0]).strftime("%d-%m-%Y %H:%M:%S")
						print("AJA KONTROLL: ")
						print("LAST TIME: {}".format(last_set_time2))
						print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

					print(self.passes[0][len(self.passes[0]) - 1])
					pass_second = self.passes[0].pop(0);
					if (len(self.passes[0]) > 0):
						if (pass_second[1] > self.passes[0][0][1]):
							self.last_move_direction = -1
						else:
							self.last_move_direction = 1
					self.moveAntenna(pass_second)
			elif (current_time > satellite_time):
				self.getNextPasses()

		else:
			time.sleep(10)
			self.getNextPasses()
			self.moveAntennaOnce(self.passes[0][0])

	def convertToCorrectRadians(self, radians):
		number_of_turns = math.floor(math.fabs(radians / (2 * math.pi)))
		if radians < 0:
			return radians + ((number_of_turns + 1) * 2 * math.pi)
		else:
			return radians - (number_of_turns * 2 * math.pi)


	def moveAntennaOnce(self, move):
		current_pos_az = self.convertToCorrectRadians(rospy.wait_for_message('/antenna/joint1_position_controller/state', JointControllerState).set_point)
		current_pos_alt = rospy.wait_for_message('/antenna/joint2_position_controller/state', JointControllerState).set_point
		next_pos_az = self.convertToCorrectRadians(move[2] - (math.pi/2.0))
		next_pos_alt = move[1] - (math.pi/2.0)

		alt_step = math.fabs(current_pos_alt - next_pos_alt) / 10.0
		az_step_alpha = math.fabs(current_pos_az - next_pos_az) / 10.0
		az_step_beta = 2 * math.pi - az_step_alpha

		for x in xrange(10):
			if (current_pos_az < next_pos_az):
				if (self.last_move_direction >= 0):
					current_pos_az -= az_step_beta
				else:
					current_pos_az += az_step_alpha
			else:
				if (self.last_move_direction >= 0):
					current_pos_az -= az_step_alpha
				else:
					current_pos_az += az_step_beta
			if (current_pos_alt < next_pos_alt):
				current_pos_alt += alt_step
			else:
				current_pos_alt -= alt_step
			self.pub1.publish(current_pos_az)		
			self.pub2.publish(current_pos_alt)
			time.sleep(0.5)

		print("SEE ON WAIT FOR MESSAGE")
		print(current_pos_az)
		# rospy.spin()

	def moveAntenna(self, move):
		self.pub1.publish(move[2]-(math.pi/2.0))
		self.pub2.publish(move[1]-(math.pi/2.0))

		# rate = rospy.Rate(100)
		# while not rospy.is_shutdown():
		# 	connections1 = self.pub1.get_num_connections()
		# 	connections2 = self.pub2.get_num_connections()
		# 	rospy.loginfo("Connections: {}, {}".format(connections1, connections2))
		# 	if (connections1 > 0 and connections2 > 0):
		# 		self.pub1.publish(move[2]-(math.pi/2.0))
		# 		self.pub2.publish(move[1]-(math.pi/2.0))
		# 		break
		# 	rate.sleep()
			# time.sleep(0.1)
		print("DONE")


	def addSatelliteToTrack(self, catalog_number, name):
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

	def getNextPasses(self):
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
			# obs.horizon = '10'
			# print(x)
			satellite = ephem.readtle(x[0], x[1], x[2])
			satellite.compute(obs)

			# satellite = ephem.readtle(lines[0], lines[1], lines[2])

			current_sat_passes = []

			# for i in range(3):
			while (len(current_sat_passes) < 3):
				pass_parts = []
				rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
				# print("PASSES {}, {}, {}".format(current_sat_passes, max_alt, obs.date))
				if math.degrees(max_alt) < 0:
					obs.date = set_time + ephem.minute
					continue

				# print(rise_time, set_time, x[0])
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
				current_sat_passes.append(pass_parts)
				obs.date = rise_time + ephem.minute
			all_passes.extend(current_sat_passes)
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


		self.passes = all_passes

	def changeAntennaState():
		if (self.is_stopped):
			self.is_stopped = False
			rospy.loginfo("Shut down antenna")
		else:
			self.is_stopped = True
			rospy.loginfo("Continue tracking")


def main():
	# addSatelliteToTrack(39161, "ESTCUBE 1")
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

	controller = AntennaController()
	controller.runProgram()

	# p = multiprocessing.Process(target=tleSchedule)
	# p.start()

	# d = multiprocessing.Process(target=runProgram)
	# d.start()

	#Kui anda ette satelliit, mis vaatev'lja kunagi ei joua, siis error  + 
	#Sujuv liikumine. URDF korda Vaadata mis pidi liikus eelmine kord ja siis liikuda vastupidi 
	#Min horizon - Vist tootab, aga kontrolli ule. Lisaks vaja kontrollida satelliitide ulelennu ajad. Tundub, et horizoni panemisega annabki ta ulelennu vastavast horizonis horizonini. Meie tahame, et ta lihtsalt skipiks need, mis ule mingi horizoni kunagi ei joua, aga hakkaks neid jalgima ikkagi nullist. For, if
	#Kui gazebo ei toota


if __name__ == '__main__':
	main()

