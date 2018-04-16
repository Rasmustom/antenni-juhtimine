#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
		open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tle.txt', 'w').close()
		self.pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
		self.pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)
		rospy.init_node('control_monitor', anonymous=True)

		while not (os.stat('/home/rasmus/catkin_ws/src/antenna_controller/tle/tle.txt').st_size > 0):
			print("No tle yet")
			time.sleep(0.5)

		self.getNextPasses()

		for x in self.passes:
			if len(x) == 0:
				print("TRUE")
			else:
				print("FALSE")

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
					print(self.passes[0][len(self.passes[0]) - 1])
					pass_second = self.passes[0].pop(0);
					if (len(self.passes[0]) > 0):
						if (pass_second[1] > self.passes[0][0][1]):
							self.last_move_direction = -1
						else:
							self.last_move_direction = 1
					self.moveAntenna(pass_second)
			elif (current_time > satellite_time):
				print
				print("CHECK TIME : satellite: {}, current: {}".format(satellite_time_string, current_time_string))
				print
				self.getNextPasses()
				self.moveAntennaOnce(self.passes[0][0])
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
		print(current_pos_az)

	def moveAntenna(self, move):
		self.pub1.publish(move[2]-(math.pi/2.0))
		self.pub2.publish(move[1]-(math.pi/2.0))
		print("DONE")

	def getNextPasses(self):
		lines = []
		for line in open('/home/rasmus/catkin_ws/src/antenna_controller/tle/tle.txt','r').readlines():
			lines.append(line)
		print("VAAAAAAAAAAAAATATATAAAA SIISA {}".format(lines))

		all_passes = []
		obs = ephem.Observer()
		obs.lat = '59.394870'
		obs.long = '24.661399'
		# obs.horizon = '10'
		satellite = ephem.readtle(lines[0], lines[1], lines[2])
		satellite.compute(obs)

		current_sat_passes = []

		while (len(all_passes) < 3):
			pass_parts = []
			rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
			# print("PASSES {}, {}, {}".format(all_passes, max_alt, obs.date))
			if (math.degrees(max_alt) < 0):
				obs.date = set_time + ephem.minute
				continue

			satellite_time = ephem.localtime(rise_time)
			if (rise_time > set_time):
				range_s = satellite.range
				sat_az = math.degrees(satellite.az)
				sat_alt = math.degrees(satellite.alt)

				print("CURRENT PASS : rise_time: {}, set_time: {}, current_time: {}, range: {}, az: {}, alt: {}".format(rise_time, set_time, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), range_s, sat_az, sat_alt ))

				turning_time = self.getTurningTime(sat_az, sat_alt) # Hetkel ei tee veel midagi, 
				# kuid hiljem loeb antenni asukohta ja arvutab, kaua aega l'heks antenni pooramiseni ja paneb selle aja rise_timele juurde.
				# See t'hendab, et kui programm naeb, et antenn ei joua kuidagi moodi isegi mootma hakata, siis ei hakka ta seda satelliiti
				# uldse jalgima.

				rise_time = ephem.Date(ephem.Date(datetime.utcnow()) + ephem.second * 10)
				print("{}, | {}".format(rise_time, set_time))

				if (rise_time > set_time):
					obs.date = set_time + ephem.minute
					continue

			while (rise_time < set_time):
				obs.date = rise_time
				satellite.compute(obs)
				pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az)), lines[0], int(lines[2].split(" ")[1])))
				rise_time = ephem.Date(rise_time + ephem.second)
			all_passes.append(pass_parts)
			obs.date = rise_time + ephem.minute
			
		print("ALL PASSES LENGTH: {}".format(len(all_passes)))
		for x in all_passes:
			if len(x) > 0:
				print(x[0])
		self.passes = all_passes

	def getTurningTime(self, sat_az, sat_alt):
		current_pos_az = self.convertToCorrectRadians(rospy.wait_for_message('/antenna/joint1_position_controller/state', JointControllerState).set_point)
		current_pos_alt = rospy.wait_for_message('/antenna/joint2_position_controller/state', JointControllerState).set_point
		leg_joint_speed = 1
		dish_joint_speed = 1
		dish_joint_time = math.fabs(sat_alt - current_pos_alt) / dish_joint_speed
		leg_joint_time = math.fabs(sat_az - current_pos_az) / leg_joint_speed
		if (dish_joint_time > leg_joint_time):
			return dish_joint_time
		else:
			return leg_joint_time

	def changeAntennaState():
		if (self.is_stopped):
			self.is_stopped = False
			rospy.loginfo("Shut down antenna")
		else:
			self.is_stopped = True
			rospy.loginfo("Continue tracking")


def main():
	controller = AntennaController()
	controller.runProgram()

	# p = multiprocessing.Process(target=tleSchedule)
	# p.start()

	# d = multiprocessing.Process(target=runProgram)
	# d.start()

	#Kui anda ette satelliit, mis vaatev'lja kunagi ei joua, siis error  + 
	#Sujuv liikumine. URDF korda Vaadata mis pidi liikus eelmine kord ja siis liikuda vastupidi 
	#Min horizon - Vist tootab, aga kontrolli ule. Lisaks vaja kontrollida satelliitide ulelennu ajad. Tundub, et horizoni panemisega annabki ta ulelennu vastavast horizonis horizonini. Meie tahame, et ta lihtsalt skipiks need, mis ule mingi horizoni kunagi ei joua, aga hakkaks neid jalgima ikkagi nullist. For, if
	#Kui gazebo ei toota +
	#Kui satelliiti j'lgima hakates on satelliit juba vaatevaljas
	# print("%s | %4.1f %5.1f | %4.1f %+6.1f | %5.1f" % \
				# 	(rise_time,
				# 		math.degrees(satellite.alt),
				# 		math.degrees(satellite.az),
				# 		math.degrees(satellite.sublat),
				# 		math.degrees(satellite.sublong),
				# 		satellite.elevation/1000.))

 
	# Kui satelliit on juba pea kohal, siis peaks samuti hakkama seda jälgima. Siin aga võiks arvestada ka olukorraga, kus antenn
	# ei jõuaks nagunii satelliidini vajaliku aja jooksul liikuda. Sellisel juhul poleks sellest hetke asukoha jälgimisest suurt kasu
	# ning antenn peaks liikuma järgmise alguspunkti peale. Seda tehes peab arvestama antenni võimaliku max kiirusega liigutamisel 
	# õigesse kohta kuluvat aega.

	# Kui algselt tööle panna, siis ei peaks ta alati samale poole minema, vaid vaatama hetke asukoha järgi, kummale poole mõislikum liikuda on.
	# Üldiselt pean rohkem kontrollima antenni hetke asukohta ja selle abil otsustama, kummale poole liikuda. Ilmselt suurem osa
	# ajast saan kasutada sama loogikat, et liigu vastupidi eelmisele, kuid on olukordi, mil see viis ei tööta ja antenn võib 
	# hakata potentsiaalselt liikuma praktiliselt ringiratast. 

	# Teha tle küsimine sagedasemaks. Nt, iga paari tunni tagant

	# Mida teha taldrikuga. Hetkel on ulemine asend 0 ja vahemik on -pi/2 - +pi/2. Siiamaani teinud nii, et lahutan pi/2, aga nii saan
	# alati ainult [hele poole liikuda

	# Seniidis

	# Refactor - Loo mingi osa funktsioone lahku


if __name__ == '__main__':
	main()

