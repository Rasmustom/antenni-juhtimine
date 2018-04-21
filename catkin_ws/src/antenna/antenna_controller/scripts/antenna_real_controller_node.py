#!/usr/bin/env python

import rospy
from antenna_msgs.msg import Antenna_command


def callback(data):
    print("PUBLISHED DATA: \n{}".format(data))


def subscribe():
    rospy.init_node('antenna_command')
    rospy.Subscriber('antenna_command', Antenna_command, callback)
    rospy.spin()


if __name__ == '__main__':
    subscribe()
