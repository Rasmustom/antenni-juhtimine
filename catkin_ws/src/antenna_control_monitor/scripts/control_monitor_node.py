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

#control_msgs/JointControllerState

def callback(msg):
	set_point = msg.set_point
	p = msg.p
	i = msg.i
	d = msg.d
	pub = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
	rate = rospy.Rate(10)
	# while not rospy.is_shutdown():
	rospy.loginfo('set_point: {}, p: {}, i: {}, d: {}'.format(set_point, p, i, d))
	pub.publish(set_point+0.01)
	# hello_str = "hello world %s" % rospy.get_time()
	# rospy.loginfo(hello_str)
	# rate.sleep()

def tleSchedule():
	schedule.every().day.at("14:00").do(getTle)
	while True:
		schedule.run_pending()
		time.sleep(60)

def getTle():
	st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
	tle = st.tle_latest(norad_cat_id=39161, ordinal=1, format='3le')

	# tle = st.tle_latest(norad_cat_id=39161, orderby='epoch desc', limit=22, format='tle')

	# with open('/home/rasmus/catkin_ws/src/antenna_control_monitor/scripts/spaceTrackTle.txt', 'w') as f:
		# f.write(tle)
	# print(tle)
	lines = tle.splitlines()
	lines[0] = lines[0][2:len(lines[0])]
	# print(lines)
	return lines
	

def test():
	lines = getTle()
	satellite = ephem.readtle(lines[0].encode("utf-8"), lines[1].encode("utf-8"), lines[2].encode("utf-8"))
	# satellite = ephem.readtle("ESTCUBE 1",
	# 		"1 39161U 13021C   18081.15771673  .00000186  00000-0  37452-4 0  9992",
	# 		"2 39161  98.0096 168.3373 0008820 346.0146  14.0820 14.72034481261645")

	obs = ephem.Observer()
	obs.lat = '59.394870'
	obs.long = '24.661399'
	open('/home/rasmus/catkin_ws/src/antenna_control_monitor/scripts/passes.txt', 'w').close()
	passes = []
	
	for x in range(10):
		pass_parts = []
		tr, azr, tt, altt, ts, azs = obs.next_pass(satellite)
		print("""Date/Time (UTC)       Alt/Azim    Lat/Long      Elev""")
		print("""========================================================""")
		first_loop = True
		first_tr = tr
		first_alt = 0
		first_az = 0
		max_tr = tr
		max_alt = 0
		max_az = 0
		last_tr = tr
		last_alt = 0
		last_az = 0
		alt = 0
		az = 0
		while tr < ts :
			obs.date = tr
			satellite.compute(obs)
			alt = math.degrees(satellite.alt)
			az = math.degrees(satellite.az)

			pass_parts.append([math.radians(alt), math.radians(az)])
			
			if first_loop:
				first_loop = False
				first_alt = alt
				first_az = az
				first_tr = tr
			if alt > max_alt:
				max_alt = alt
				max_az = az
				max_tr = tr
			# print("%s | %4.1f %5.1f | %4.1f %+6.1f | %5.1f" % \
			# 	(tr,
			# 		math.degrees(satellite.alt),
			# 		math.degrees(satellite.az),
			# 		math.degrees(satellite.sublat),
			# 		math.degrees(satellite.sublong),
			# 		satellite.elevation/1000.))
			# print("%s %4.1f %5.1f" % (tr, math.degrees(satellite.alt), math.degrees(satellite.az)))
			last_tr = tr
			tr = ephem.Date(tr + ephem.second)
		passes.append(pass_parts)
		last_az = az
		last_alt = alt
		print("%s | %4.1f %5.1f" % (first_tr, first_alt, first_az))
		print("%s | %4.1f %5.1f" % (max_tr, max_alt, max_az))
		print("%s | %4.1f %5.1f" % (last_tr, last_alt, last_az))

		with open('/home/rasmus/catkin_ws/src/antenna_control_monitor/scripts/passes.txt', 'a') as f:
			print("passes.txt")
			f.write("""Date/Time (UTC)       Alt/Azim    Lat/Long      Elev\n""")
			f.write("""========================================================\n""")
			f.write("%s | %4.1f %5.1f \n" % (first_tr, first_alt, first_az))
			f.write("%s | %4.1f %5.1f \n" % (max_tr, max_alt, max_az))
			f.write("%s | %4.1f %5.1f \n\n" % (last_tr, last_alt, last_az))

		obs.date = tr + ephem.minute
	print(satellite.sublong, satellite.sublat)
	# print(passes)
	return passes

def moveAntenna(passes):
	starttime = time.time()
	pub1 = rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10)
	pub2 = rospy.Publisher("/antenna/joint2_position_controller/command", Float64, queue_size=10)

	for j in passes:
		for i in j:
			# rospy.Subscriber("/antenna/joint1_position_controller/state", JointControllerState, smth)
			print(i)
			pub1.publish(i[1]-1.571)
			pub2.publish(i[0]-1.571)
			time.sleep(0.1 - ((time.time() - starttime) % 0.1))
	
def smth(msg):
	rospy.loginfo('set_point: {}'.format(msg.set_point))

def main():

	# with open('tle.txt') as f:
	# 	print(f)

	# orb = Orbital("Suomi NPP")
	# now = datetime.utcnow()
	# print(orb.get_position(now))

	# tle = tlefile.read('ISS', 'tle.txt')
	# print(tle.inclination)

	# orb = Orbital('ISS', 'tle.txt')
	# now = datetime.utcnow()
	# print(orb.get_position(now))

	rospy.init_node('control_monitor')
	# rospy.Subscriber("/antenna/joint1_position_controller/state", JointControllerState, smth)

	passes = test()
	# getTle()

	moveAntenna(passes)

	rospy.spin()

	#st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')

	#print(st.tle_latest(norad_cat_id=[25544, 41335, 39161], ordinal=1, format='tle'))

	# rospy.init_node('control_monitor')
	# rospy.Publisher("/antenna/joint1_position_controller/command", Float64, queue_size=10).publish(1)
	# rospy.Subscriber("/antenna/joint1_position_controller/state", JointControllerState, callback)


if __name__ == '__main__':
	main()