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

# class Helper():
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

#     def convertToCorrectRadians(self, radians):
#         number_of_turns = math.floor(math.fabs(radians / (2 * math.pi)))
#         if radians < 0:
#             return radians + ((number_of_turns + 1) * 2 * math.pi)
#         else:
#             return radians - (number_of_turns * 2 * math.pi)

#     def getTurningTime(self, sat_az, sat_alt):
#         current_pos_az = self.convertToCorrectRadians(rospy.wait_for_message('/antenna/joint1_position_controller/state', JointControllerState).set_point)
#         current_pos_alt = rospy.wait_for_message('/antenna/joint2_position_controller/state', JointControllerState).set_point
#         leg_joint_speed = 1.2  # deg/s - Hetkel on kiirus ainult oletatud. Kuna Andruse kirjast selgus, et anten voiks 360 kraadi 
#         # poorata umbes 5 minutiga, siis sai leida kiiruse deg/s = 360 / 5 / 60 = 1.2. Taldriku kiirust ei tea uldse, nii et see
#         # on panud ajutiselt vaga suureks, et loogikat segama ei hakkaks.
#         dish_joint_speed = 10000
#         dish_joint_time = math.fabs(sat_alt - math.degrees(current_pos_alt)) / dish_joint_speed
#         leg_joint_time = math.fabs(sat_az - math.degrees(current_pos_az)) / leg_joint_speed
#         if (dish_joint_time > leg_joint_time):
#             return dish_joint_time
#         else:
#             return leg_joint_time

#     def changeAntennaState(self):
#         if (self.is_stopped):
#             self.is_stopped = False
#             rospy.loginfo("Shut down antenna")
#         else:
#             self.is_stopped = True
#             rospy.loginfo("Continue tracking")


# def main():


# if __name__ == '__main__':
#     main()
