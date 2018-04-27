#!/usr/bin/env python

import rospy
from spacetrack import SpaceTrackClient
from std_msgs.msg import Int64
import tle_getter_node
import ephem


class SatelliteChooser(object):
    """docstring for SatelliteChooser"""
    def __init__(self):
        pass

    def doesSatellitePass(self, tle, catalog_number):
        tle_lines = tle[2:].split('\n')
        obs = ephem.Observer()
        obs.lat = '59.394870'
        obs.long = '24.661399'
        # obs.horizon = '10'
        satellite = ephem.readtle(tle_lines[0], tle_lines[1], tle_lines[2])
        try:
            obs.next_pass(satellite)
        except ValueError:
            rospy.loginfo("Satellite with catalog number {} is never above horizon".format(catalog_number))
            return False
        else:
            return True

    def addSatelliteToTrack(self, catalog_number):
        current_satellite = 0
        for line in open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/current_satellite.txt', 'r').readlines():
            current_satellite = line
        if not int(current_satellite) == catalog_number:
            with open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/current_satellite.txt', 'w') as f:
                f.write("{}".format(catalog_number))

    def callback(self, data):
        catalog_number = data.data
        st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
        tle = st.tle_latest(norad_cat_id=catalog_number, ordinal=1, format='3le').encode("utf-8").strip()
        print(tle)
        if not (tle == ""):
            print(data)
            if (self.doesSatellitePass(tle, catalog_number)):
                self.addSatelliteToTrack(catalog_number)
                tle_getter_node.TLEGetter().formatTle(tle)
        else:
            print("{}: Wrong Catalog Number".format(catalog_number))

    def chooseSatellite(self):
        rospy.init_node('satellite_chooser')
        rospy.Subscriber('satellite_chooser', Int64, self.callback)
        rospy.spin()


if __name__ == '__main__':
    SatelliteChooser().chooseSatellite()
