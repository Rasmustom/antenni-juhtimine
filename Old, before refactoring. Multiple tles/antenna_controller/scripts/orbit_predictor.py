#!/usr/bin/env python

from orbit_predictor.sources import EtcTLESource
from orbit_predictor.locations import EST
import datetime

source = EtcTLESource(filename='/home/rasmus/catkin_ws/src/antenna_control_monitor/tle/tle.txt')
predictor = source.get_predictor("ISS")
print predictor.get_next_pass(EST)

predicted_pass = _

position = predictor.get_position(predicted_pass.aos)

print EST.is_visible(position)

position_delta = predictor.get_position(predicted_pass.los + datetime.timedelta(minutes=20))

print EST.is_visible(position_delta)

tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)

print predictor.get_next_pass(EST, tomorrow, max_elevation_gt=20)