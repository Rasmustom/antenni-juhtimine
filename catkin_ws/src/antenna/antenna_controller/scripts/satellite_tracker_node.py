#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from antenna_msgs.msg import Antenna_command
from antenna_msgs.msg import Antenna_position
from antenna_msgs.msg import Weather_information
from datetime import datetime
import math
import ephem
import time
import schedule
import os

# control_msgs/JointControllerState


class SatelliteTracker():
    """docstring for SatelliteTracker"""
    def __init__(self):
        # super(AntennaController, self).__init__()
        # Finals:
        self.SECONDS_PER_MOVE = 5
        self.MAX_LEG_JOINT_ANGULAR_VELOCITY = math.radians(1.2)  # deg/s - Hetkel on kiirus ainult oletatud. Kuna Andruse kirjast selgus, et anten voiks 360 kraadi
        # poorata umbes 5 minutiga, siis sai leida kiiruse deg/s = 360 / 5 / 60 = 1.2. Taldriku kiirust ei tea uldse, nii et see
        # on panud ajutiselt vaga suureks, et loogikat segama ei hakkaks.
        self.MAX_DISH_JOINT_ANGULAR_VELOCITY = 10000
        self.GROUND_STATION_LATITUDE = '59.394870'
        self.GROUND_STATION_LONGITUDE = '24.661399'
        self.GROUND_STATION_ELEVATION = 1
        self.MIN_SATELLITE_ELEVATION = 0
        self.LEG_JOINT = "leg"
        self.DISH_JOINT = "dish"

        # Variables:
        self.next_pass = []
        self.publish_command = ""
        self.last_move_direction = 0
        self.is_stopped = False
        self.is_zenith = False
        self.max_elev_time = ''
        self.max_elev = 0
        self.last_leg_joint_velocity = 0
        self.last_dish_joint_velocity = 0

    def runProgram(self):
        open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/tle.txt', 'w').close()
        self.publish_command = rospy.Publisher("/antenna/antenna_command", Antenna_command, queue_size=10)
        rospy.init_node('satellite_tracker', anonymous=True)

        while not (os.stat('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/tle.txt').st_size > 0):
            print("No tle yet")
            time.sleep(0.5)

        self.getNextPasses()

        self.moveAntennaOnce(self.next_pass[0])

        schedule.every(0.5).seconds.do(self.checkTime)
        while True:
            schedule.run_pending()
            time.sleep(0.5)

    def checkTime(self):
        if (self.is_stopped):
            self.getWeatherInfo()
            return
        if (len(self.next_pass) > 0):
            self.getWeatherInfo()
            for line in open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/current_satellite.txt', 'r').readlines():
                if not (int(line) == self.next_pass[0][4]):
                    print("SAT HAS CHANGED {}, {}".format(line, self.next_pass[0][4]))
                    self.getNextPasses()
                    self.moveAntennaOnce(self.next_pass[0])
                break
            satellite_time = ephem.localtime(self.next_pass[0][0])
            current_time = datetime.now()
            satellite_time_string = satellite_time.strftime("%d-%m-%Y %H:%M:%S")
            current_time_string = current_time.strftime("%d-%m-%Y %H:%M:%S")
            print("Time until LOS: {}".format(len(self.next_pass) * self.SECONDS_PER_MOVE))

            print("{}\n{} {}".format(current_time_string, satellite_time_string, self.next_pass[0][3]))
            # print(current_time_string + "\n" + satellite_time_string + " " + self.next_pass[0][3])
            if (current_time_string == satellite_time_string):
                print(self.next_pass[len(self.next_pass) - 1])
                pass_second = self.next_pass.pop(0)
                if (len(self.next_pass) > 0):
                    if (pass_second[1] > self.next_pass[0][1]):
                        self.last_move_direction = -1
                    else:
                        self.last_move_direction = 1
                move_leg = self.getLegMove(pass_second)
                move_dish = self.getDishMove(pass_second)
                self.makeMovement(move_leg, move_dish, self.SECONDS_PER_MOVE)
            elif (current_time > satellite_time):
                print
                print("CHECK TIME : satellite: {}, current: {}".format(satellite_time_string, current_time_string))
                print
                self.last_leg_joint_velocity = 0
                self.last_dish_joint_velocity = 0
                self.getNextPasses()
                self.moveAntennaOnce(self.next_pass[0])
        else:
            self.last_leg_joint_velocity = 0
            self.last_dish_joint_velocity = 0
            time.sleep(10)
            self.getNextPasses()
            self.moveAntennaOnce(self.next_pass[0])

    def getWeatherInfo(self):
        # current_weather_data = rospy.wait_for_message('/antenna/weather_information', Weather_information)
        current_weather_data = rospy.get_param('weather_information')
        print(current_weather_data)

    def getLegMove(self, move):
        leg_move = move[2]
        if (math.degrees(self.max_elev) > 89):
            leg_move = self.getCurrentPosition()[0]
        return leg_move

    def getDishMove(self, move):
        dish_move = move[1]
        if (math.degrees(self.max_elev) > 89):
            if (self.max_elev_time < move[0]):
                dish_move = math.pi - move[2]
        return dish_move

    def convertToCorrectRadians(self, radians):
        number_of_turns = math.floor(math.fabs(radians / (2 * math.pi)))
        if radians < 0:
            return radians + ((number_of_turns + 1) * 2 * math.pi)
        else:
            return radians - (number_of_turns * 2 * math.pi)

    def moveAntennaOnce(self, move):
        current_position_data = self.getCurrentPosition()
        start_pos_az = current_position_data[0]
        start_pos_alt = current_position_data[1]

        new_current_pos_az = start_pos_az
        new_current_pos_alt = start_pos_alt
        print("CURRENT POSITION AZIMUTH : {}".format(new_current_pos_az))
        next_pos_az = self.convertToCorrectRadians(move[2])
        next_pos_alt = move[1]

        alt_step = math.fabs(new_current_pos_alt - next_pos_alt) / 10.0
        az_step_alpha = math.fabs(new_current_pos_az - next_pos_az) / 10.0
        az_step_beta = 2 * math.pi - az_step_alpha

        for x in xrange(10):
            if (new_current_pos_az < next_pos_az):
                if (self.last_move_direction >= 0):
                    new_current_pos_az -= az_step_beta
                else:
                    new_current_pos_az += az_step_alpha
            else:
                if (self.last_move_direction >= 0):
                    new_current_pos_az -= az_step_alpha
                else:
                    new_current_pos_az += az_step_beta
            if (new_current_pos_alt < next_pos_alt):
                new_current_pos_alt += alt_step
            else:
                new_current_pos_alt -= alt_step
            new_current_pos_az = self.convertToCorrectRadians(new_current_pos_az)

            turning_time = self.getTurningTime(new_current_pos_az, new_current_pos_alt)
            self.makeMovement(new_current_pos_az, new_current_pos_alt, turning_time)
            time.sleep(turning_time)
        self.stopAntenna()
        self.adjustAntenna(start_pos_az, start_pos_alt)
        self.last_leg_joint_velocity = 0
        self.last_dish_joint_velocity = 0

    def adjustAntenna(self, sat_az, sat_alt):
        current_pos_az = self.getCurrentPosition()[0]
        while (math.fabs(current_pos_az - sat_az) > math.radians(0.5)):
            self.makeMovement(sat_az, sat_alt, 1)
            print("ADJUSTING ANTENNA: {}, {}, {}".format(sat_az, sat_alt, current_pos_az))
            current_pos_az = self.getCurrentPosition()[0]

    def getDisplacementAz(self, az1, az2):
        displacement = math.fabs(az1 - az2)
        if (displacement > math.pi):
            return 2 * math.pi - displacement
        return displacement

    def makeMovement(self, az, alt, seconds):
        current_position_data = self.getCurrentPosition()
        current_pos_az = current_position_data[0]
        current_pos_alt = current_position_data[1]

        # displacement_az = math.fabs(az - current_pos_az)
        displacement_az = self.getDisplacementAz(az, current_pos_az)
        displacement_alt = math.fabs(alt - current_pos_alt)

        leg_acceleration = self.calcAcceleration(displacement_az, self.last_leg_joint_velocity, seconds, 1)
        dish_acceleration = self.calcAcceleration(displacement_alt, self.last_dish_joint_velocity, seconds, 1)
        self.last_leg_joint_velocity = self.calcVelocity(self.last_leg_joint_velocity, displacement_az, leg_acceleration, 1)
        self.last_dish_joint_velocity = self.calcVelocity(self.last_dish_joint_velocity, displacement_alt, dish_acceleration, 1)
        print("TIME: \n\t{}".format(seconds))
        print("POSITIONS: \n\tLEG: {}, {}\n\tDISH: {}, {}".format(az, current_pos_az, alt, current_pos_alt))
        print("ACCELERATIONS: \n\tLEG: {}\n\tDISH: {}".format(leg_acceleration, dish_acceleration))
        print("VELOCITIES: \n\tLEG: {}\n\tDISH: {}".format(self.last_leg_joint_velocity, self.last_dish_joint_velocity))
        self.publishCommand(self.last_leg_joint_velocity, self.last_dish_joint_velocity, az, alt, leg_acceleration, dish_acceleration)

    def calcVelocity(self, initial_velocity, displacement, acceleration, radius=1):
        print("VELOCITY EQUATION:\n\tinit_velocity: {}\n\tradius: {}\n\displacement: {}\n\tacceleration: {}".format(initial_velocity, radius, displacement, acceleration))
        # return (initial_velocity + acceleration * seconds) * radius
        return math.sqrt(math.pow(initial_velocity, 2) + (2 * acceleration * displacement))

    def calcAcceleration(self, displacement, initial_velocity, seconds, radius=1):
        print("ACCELERATION EQUATION:\n\tdisplacement: {}\n\tinit_velocity: {}\n\tseconds: {}\n\tradius: {}".format(displacement, initial_velocity, seconds, radius))
        return (((2 * displacement) - (2 * initial_velocity * seconds)) / math.pow(seconds, 2)) * radius

    def publishCommand(self, leg_linear_velocity, dish_linear_velocity, leg_angle, dish_angle, leg_acceleration=0, dish_acceleration=0):
        msg = Antenna_command()
        msg.leg_linear_velocity = leg_linear_velocity
        msg.dish_linear_velocity = dish_linear_velocity
        msg.leg_angle = leg_angle
        msg.dish_angle = dish_angle
        msg.leg_linear_acceleration = leg_acceleration
        msg.dish_linear_acceleration = dish_acceleration
        self.publish_command.publish(msg)

    def getNextPasses(self):
        data = SatelliteInfoFreshener().getNextPasses()
        self.max_elev_time = data['max_elev_time']
        self.max_elev = data['max_elev']
        self.next_pass = data['next_pass']
        print(data)

    # TODO
    def getTurningTime(self, sat_az, sat_alt):
        current_position_data = self.getCurrentPosition()
        current_pos_az = current_position_data[0]
        current_pos_alt = current_position_data[1]

        # VAATA! DISPLACEMENT ON VALE

        dish_joint_time = self.findTime(self.last_dish_joint_velocity, self.MAX_DISH_JOINT_ANGULAR_VELOCITY, math.fabs(sat_alt - current_pos_alt))
        leg_joint_time = self.findTime(self.last_leg_joint_velocity, self.MAX_LEG_JOINT_ANGULAR_VELOCITY, math.fabs(sat_az - current_pos_az))
        # dish_joint_time = 2 * math.fabs(sat_alt - current_pos_alt) / (self.last_dish_joint_velocity + self.MAX_DISH_JOINT_ANGULAR_VELOCITY)
        # leg_joint_time = 2 * math.fabs(sat_az - current_pos_az) / (self.last_leg_joint_velocity + self.MAX_LEG_JOINT_ANGULAR_VELOCITY)
        print("===============================================================")
        print("\nMOVE ANTENNA ONCE: \n\tCurrent: {}, {}\n\tNew:{}, {}\n\tSeconds: {}".format(current_pos_az, current_pos_alt, sat_az, sat_alt, leg_joint_time))

        if (dish_joint_time > leg_joint_time):
            return dish_joint_time
        else:
            return leg_joint_time

    def findTime(self, initial_velocity, final_velocity, displacement):
        if (initial_velocity == final_velocity):
            return displacement / final_velocity
        if (displacement >= 0):
            return 2 * displacement / (final_velocity + initial_velocity)
        else:
            return -2 * displacement / (final_velocity - initial_velocity)

    def changeAntennaState(self):
        if (self.is_stopped):
            self.is_stopped = False
            self.stopAntenna()
            rospy.loginfo("Shut down antenna")
        else:
            self.is_stopped = True
            rospy.loginfo("Continue tracking")

    def stopAntenna(self):
        time = 1
        initial_leg_velocity = self.last_leg_joint_velocity
        initial_dish_velocity = self.last_dish_joint_velocity
        current_position_data = self.getCurrentPosition()
        current_pos_az = current_position_data[0]
        current_pos_alt = current_position_data[1]

        leg_acceleration = initial_dish_velocity * -1 / time
        dish_acceleration = initial_dish_velocity * -1 / time
        leg_angle = self.convertToCorrectRadians(current_pos_az + (initial_leg_velocity * time / 2))    # Oleneb suunast, kas liita voi lahutada
        dish_angle = current_pos_alt + (initial_dish_velocity * time / 2)

        self.publishCommand(0, 0, leg_angle, dish_angle, leg_acceleration, dish_acceleration)

    def getCurrentPosition(self):
        current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
        current_pos_az = self.convertToCorrectRadians(current_position_data.leg_angle)
        current_pos_alt = current_position_data.dish_angle
        return (current_pos_az, current_pos_alt)


class SatelliteInfoFreshener():
    """docstring for SatelliteInfoFreshener"""
    def __init__(self):
        self.GROUND_STATION_LATITUDE = '59.394870'
        self.GROUND_STATION_LONGITUDE = '24.661399'
        self.GROUND_STATION_ELEVATION = 1
        self.MIN_SATELLITE_ELEVATION = 0
        self.SECONDS_PER_MOVE = 5

    def getNextPasses(self):
        final_max_elev_time = ""
        final_max_elev = 0
        lines = []
        for line in open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/tle.txt', 'r').readlines():
            lines.append(line)
        print("Get next passes tle: {}".format(lines))

        pass_parts = []
        obs = ephem.Observer()
        obs.lat = self.GROUND_STATION_LATITUDE
        obs.long = self.GROUND_STATION_LONGITUDE
        obs.elevation = self.GROUND_STATION_ELEVATION

        satellite = ephem.readtle(lines[0], lines[1], lines[2])
        satellite.compute(obs)

        while (len(pass_parts) == 0):
            pass_parts = []
            rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
            final_max_elev_time = max_alt_time
            final_max_elev = max_alt
            if (math.degrees(max_alt) < self.MIN_SATELLITE_ELEVATION):
                obs.date = set_time + ephem.minute
                continue

            if (rise_time > set_time):
                print("CURRENT PASS : \n\trise_time: {},\n\t set_time: {},\n\t current_time: {},\n\t az: {},\n\t alt: {}".format(rise_time, set_time, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), math.degrees(satellite.az), math.degrees(satellite.alt)))

                turning_time = SatelliteTracker.getTurningTime(math.radians(math.degrees(satellite.az)), math.radians(math.degrees(satellite.alt)))
                rise_time = ephem.Date(ephem.Date(datetime.utcnow()) + ephem.second * (turning_time + 30))

                if (rise_time > set_time):
                    obs.date = set_time + ephem.minute
                    continue

            while (rise_time < set_time):
                obs.date = rise_time
                satellite.compute(obs)
                pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az)), lines[0], int(lines[2].split(" ")[1])))
                rise_time = ephem.Date(rise_time + ephem.second * self.SECONDS_PER_MOVE)

        antenna_info = {
            "max_elev_time": final_max_elev_time,
            "max_elev": final_max_elev,
            "next_pass": pass_parts
        }
        print(antenna_info)
        return antenna_info


def main():
    controller = SatelliteTracker()
    controller.runProgram()

    # p = multiprocessing.Process(target=tleSchedule)
    # p.start()

    # d = multiprocessing.Process(target=runProgram)
    # d.start()

    # Sujuv liikumine. URDF korda Vaadata mis pidi liikus eelmine kord ja siis liikuda vastupidi
    # Kui gazebo ei toota +

    # Kui algselt tööle panna, siis ei peaks ta alati samale poole minema, vaid vaatama hetke asukoha järgi, kummale poole mõislikum liikuda on.
    # Üldiselt pean rohkem kontrollima antenni hetke asukohta ja selle abil otsustama, kummale poole liikuda. Ilmselt suurem osa
    # ajast saan kasutada sama loogikat, et liigu vastupidi eelmisele, kuid on olukordi, mil see viis ei tööta ja antenn võib
    # hakata potentsiaalselt liikuma praktiliselt ringiratast.  - Ei saa enne teha, kui tean reaalset antenni andmeid

    # Seniidis - 1-3 h

    # Refactor - Loo mingi osa funktsioone lahku - 1h


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
