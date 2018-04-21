#!/usr/bin/env python

import rospy
from spacetrack import SpaceTrackClient
import time
import schedule


def tleSchedule():
    time.sleep(1)
    getTles()

    schedule.every(4).hours.do(getTles)
    while True:
        schedule.run_pending()
        time.sleep(60)

    # schedule.every().day.at("14:00").do(getTles)
    # while True:
    #   print("hey")
    #   schedule.run_pending()
    #   time.sleep(60)


def getTles():
    catalog_number = 39161
    for line in open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/current_satellite.txt','r').readlines():
        catalog_number = int(line)
    st = SpaceTrackClient('rasmustomsen@hotmail.com', '!kK!Ft3-W6sKGa8X')
    tle = st.tle_latest(norad_cat_id=catalog_number, ordinal=1, format='3le').encode("utf-8").strip()
    rospy.loginfo(tle)
    formatTle(tle)


def formatTle(tle):
    tles_string = tle[2:]

    print(tles_string)
    print(len(tles_string.split("\n")))
    with open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/tle.txt', 'w') as f:
        f.write(tles_string)


if __name__ == '__main__':
    tleSchedule()