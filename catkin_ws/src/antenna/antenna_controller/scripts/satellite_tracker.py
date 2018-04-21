# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import rospy
# from std_msgs.msg import Float64
# from std_msgs.msg import String
# from antenna_msgs.msg import Antenna_command
# from control_msgs.msg import JointControllerState
# from spacetrack import SpaceTrackClient
# from datetime import datetime
# from operator import itemgetter
# import math
# import ephem
# import time
# import schedule
# import multiprocessing
# import os
# import json
# import re

# #control_msgs/JointControllerState

# class SatelliteTracker():
#     """docstring for AntennaController"""
#     def __init__(self):
#         # super(AntennaController, self).__init__()
#         self.next_pass = []
#         self.pub1 = ""
#         self.pub2 = ""
#         self.publish_command = ""
#         self.last_move_direction = 0
#         self.is_stopped = False
#         self.is_zenith = False
#         self.seconds_per_move = 5

#     def getNextPasses(self):
#         lines = []
#         for line in open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/tle.txt', 'r').readlines():
#             lines.append(line)
#         print("VAAAAAAAAAAAAATATATAAAA SIISA {}".format(lines))

#         all_passes = []
#         pass_parts = []
#         obs = ephem.Observer()
#         obs.lat = '59.394870'
#         obs.long = '24.661399'
#         # obs.horizon = '10'
#         satellite = ephem.readtle(lines[0], lines[1], lines[2])
#         satellite.compute(obs)

#         while (len(pass_parts) == 0):
#             rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)

#             if (math.degrees(max_alt) < 0):  # Minimaalne kõrgus, millega üldse trackima hakata
#                 obs.date = set_time + ephem.minute
#                 continue

#             if (rise_time > set_time):  # Olukord tekib siis, kui hakatakse trackima samal ajal, kui satelliit vaateväljas on
#                 range_s = satellite.range
#                 sat_az = math.degrees(satellite.az)
#                 sat_alt = math.degrees(satellite.alt)

#                 print("CURRENT PASS : rise_time: {}, set_time: {}, current_time: {}, range: {}, az: {}, alt: {}".format(rise_time, set_time, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), range_s, sat_az, sat_alt))

#                 turning_time = self.getTurningTime(sat_az, sat_alt)
#                 # loeb antenni asukohta ja arvutab, kaua aega l'heks antenni pooramiseni ja paneb selle aja rise_timele juurde.
#                 # See t'hendab, et kui programm naeb, et antenn ei joua kuidagi moodi isegi mootma hakata, siis ei hakka ta seda satelliiti
#                 # uldse jalgima.
#                 print("TURNING TIME : {} SECONDS".format(turning_time))

#                 # Lisasin rise_timele veel ise 10 sekundit eksimisruumi ja ruumi muude tegevuste l'biviimiseks
#                 rise_time = ephem.Date(ephem.Date(datetime.utcnow()) + ephem.second * (turning_time + 10))
#                 print("{}, | {}".format(rise_time, set_time))

#                 if (rise_time > set_time):  # Kui peale pööramisaja arvutamist on näha, et ei õnnestu satelliiti järgima hakata
#                     obs.date = set_time + ephem.minute
#                     continue

#             while (rise_time < set_time):
#                 obs.date = rise_time
#                 satellite.compute(obs)
#                 pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az)), lines[0], int(lines[2].split(" ")[1])))
#                 rise_time = ephem.Date(rise_time + ephem.second * self.seconds_per_move)
#             # obs.date = rise_time + ephem.minute

#         print("ALL PASSES LENGTH: {}".format(len(all_passes)))
#         return pass_parts


# def main():
    

# if __name__ == '__main__':
#     main()
