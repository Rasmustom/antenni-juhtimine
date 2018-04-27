#!/usr/bin/env python

import rospy
from antenna_msgs.msg import Antenna_command
from std_msgs.msg import Float64


class AntennaController():
    """docstring for AntennaController"""
    def __init__(self):
        self.publish_leg_joint = ""
        self.publish_dish_joint = ""

    def moveAntennaGazebo(self, new_az, new_alt):
        self.publish_leg_joint.publish(new_az)
        self.publish_dish_joint.publish(new_alt)

    def callback(self, data):
        self.moveAntennaGazebo(data.leg_angle, data.dish_angle)
        print("PUBLISHED DATA: \n{}".format(data))

    def subscribe(self):
        # rospy.init_node('antenna_command')
        rospy.Subscriber('/antenna/antenna_command', Antenna_command, self.callback)
        rospy.spin()

    def main(self):
        self.publish_leg_joint = rospy.Publisher("/antenna/leg_joint_position_controller/command", Float64, queue_size=10)
        self.publish_dish_joint = rospy.Publisher("/antenna/dish_joint_position_controller/command", Float64, queue_size=10)
        rospy.init_node('antenna_controller', anonymous=False)
        self.subscribe()


if __name__ == '__main__':
    AntennaController().main()
