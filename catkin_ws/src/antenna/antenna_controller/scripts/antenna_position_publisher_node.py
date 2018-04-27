#!/usr/bin/env python

import rospy
from antenna_msgs.msg import Antenna_position
from sensor_msgs.msg import JointState


class AntennaPositionPublisher():
    """docstring for AntennaPositionPublisher"""
    def __init__(self):
        self.publish_antenna_position = ""

    def publishPosition(self, leg_angle, dish_angle):
        msg = Antenna_position()
        msg.leg_angle = leg_angle
        msg.dish_angle = dish_angle
        self.publish_antenna_position.publish(msg)

    def callback(self, data):
        antenna_position = data.position
        self.publishPosition(antenna_position[1], antenna_position[0])

    def subscribe(self):
        rospy.Subscriber('/antenna/joint_states', JointState, self.callback)
        rospy.spin()

    def main(self):
        self.publish_antenna_position = rospy.Publisher("/antenna/antenna_position", Antenna_position, queue_size=10)
        rospy.init_node('antenna_position', anonymous=False)
        self.subscribe()


if __name__ == '__main__':
    AntennaPositionPublisher().main()
