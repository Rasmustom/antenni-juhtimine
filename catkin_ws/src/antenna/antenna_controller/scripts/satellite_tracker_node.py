#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from antenna_msgs.msg import Antenna_command
from antenna_msgs.msg import Antenna_position
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
        self.seconds_per_move = 5
        self.max_leg_joint_angular_velocity = 1.2  # deg/s - Hetkel on kiirus ainult oletatud. Kuna Andruse kirjast selgus, et anten voiks 360 kraadi
        # poorata umbes 5 minutiga, siis sai leida kiiruse deg/s = 360 / 5 / 60 = 1.2. Taldriku kiirust ei tea uldse, nii et see
        # on panud ajutiselt vaga suureks, et loogikat segama ei hakkaks.
        self.max_dish_joint_angular_velocity = 10000
        self.ground_station_latitude = '59.394870'
        self.ground_station_longitude = '24.661399'
        self.ground_station_elevation = 1
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
            return
        if (len(self.next_pass) > 0):
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
            print("Time until LOS: {}".format(len(self.next_pass) * self.seconds_per_move))

            print(current_time_string + "\n" + satellite_time_string + " " + self.next_pass[0][3])
            if (current_time_string == satellite_time_string):
                if (len(self.next_pass) > 0):
                    print(self.next_pass[len(self.next_pass) - 1])
                    pass_second = self.next_pass.pop(0)
                    if (len(self.next_pass) > 0):
                        if (pass_second[1] > self.next_pass[0][1]):
                            self.last_move_direction = -1
                        else:
                            self.last_move_direction = 1
                    move_leg = self.getLegMove(pass_second)
                    move_dish = self.getDishMove(pass_second)
                    self.makeMovement(move_leg, move_dish, self.seconds_per_move)
                    # self.moveAntenna(pass_second)
            elif (current_time > satellite_time):
                print
                print("CHECK TIME : satellite: {}, current: {}".format(satellite_time_string, current_time_string))
                print
                self.getNextPasses()
                self.moveAntennaOnce(self.next_pass[0])
        else:
            time.sleep(10)
            self.getNextPasses()
            self.moveAntennaOnce(self.next_pass[0])

    def convertToCorrectRadians(self, radians):
        number_of_turns = math.floor(math.fabs(radians / (2 * math.pi)))
        if radians < 0:
            return radians + ((number_of_turns + 1) * 2 * math.pi)
        else:
            return radians - (number_of_turns * 2 * math.pi)

    def moveAntennaOnce(self, move):
        current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
        start_pos_az = self.convertToCorrectRadians(current_position_data.leg_angle)
        start_pos_alt = current_position_data.dish_angle
        new_pos_az = start_pos_az
        new_pos_alt = start_pos_alt
        print("CURRENT POSITION AZIMUTH : {}".format(new_pos_az))
        next_pos_az = self.convertToCorrectRadians(move[2])
        next_pos_alt = move[1]

        alt_step = math.fabs(new_pos_alt - next_pos_alt) / 10.0
        az_step_alpha = math.fabs(new_pos_az - next_pos_az) / 10.0
        az_step_beta = 2 * math.pi - az_step_alpha

        leg_velocity = 0
        dish_velocity = 0
        for x in xrange(10):
            if (new_pos_az < next_pos_az):
                if (self.last_move_direction >= 0):
                    new_pos_az -= az_step_beta
                else:
                    new_pos_az += az_step_alpha
            else:
                if (self.last_move_direction >= 0):
                    new_pos_az -= az_step_alpha
                else:
                    new_pos_az += az_step_beta
            if (new_pos_alt < next_pos_alt):
                new_pos_alt += alt_step
            else:
                new_pos_alt -= alt_step
            new_pos_az = self.convertToCorrectRadians(new_pos_az)
            turning_time = self.getTurningTime(new_pos_az, new_pos_alt)

            # current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
            # current_pos_az = self.convertToCorrectRadians(current_position_data.leg_angle)
            # current_pos_alt = current_position_data.dish_angle
            # displacement_az = math.fabs(new_pos_az - current_pos_az)
            # displacement_alt = math.fabs(new_pos_alt - current_pos_alt)
            # leg_acceleration = self.calcAcceleration(displacement_az, leg_velocity, turning_time, 1)
            # dish_acceleration = self.calcAcceleration(displacement_alt, dish_velocity, turning_time, 1)
            # leg_velocity = self.calcVelocity2(leg_velocity, 1, turning_time, leg_acceleration)
            # dish_velocity = self.calcVelocity2(dish_velocity, 1, turning_time, dish_acceleration)
            # print("POSITIONS: \n\tLEG: {}, {}\n\tDISH: {}, {}".format(new_pos_az, current_pos_az, new_pos_alt, current_pos_alt))
            # print("ACCELERATIONS: \n\tLEG: {}\n\tDISH: {}".format(leg_acceleration, dish_acceleration))
            # print("VELOCITIES: \n\tLEG: {}\n\tDISH: {}".format(leg_velocity, dish_velocity))
            self.makeMovement(new_pos_az, new_pos_alt, turning_time)
            # self.calculateVelocity(new_pos_az, new_pos_alt, turning_time)

            # time.sleep(turning_time)
            time.sleep(5)

    def moveAntenna(self, move):
        print("MAX ELEVATION TIME: {} | CURRENT TIME: {} | {}".format(self.max_elev_time, move[0], self.max_elev_time < move[0]))

        leg_move = move[2]
        dish_move = move[1]

        print("MAX ELEVATION : {}, Dish move = {}".format(math.degrees(self.max_elev), dish_move))
        if (math.degrees(self.max_elev) > 89):
            current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
            leg_move = self.convertToCorrectRadians(current_position_data.leg_angle)
            # current_pos_alt = current_position_data.dish_angle
            # leg_move = self.convertToCorrectRadians(rospy.wait_for_message('/antenna/leg_joint_position_controller/state', JointControllerState).set_point)
            if (self.max_elev_time < move[0]):
                dish_move = math.pi - move[2]
        print("AFTER IFS DISH MOVE: {}".format(dish_move))

        self.calculateVelocity(leg_move, dish_move, self.seconds_per_move)

    def getLegMove(self, move):
        leg_move = move[2]
        if (math.degrees(self.max_elev) > 89):
            current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
            leg_move = self.convertToCorrectRadians(current_position_data.leg_angle)
        return leg_move

    def getDishMove(self, move):
        dish_move = move[1]
        if (math.degrees(self.max_elev) > 89):
            if (self.max_elev_time < move[0]):
                dish_move = math.pi - move[2]
        return dish_move

    def calculateVelocity(self, az, alt, seconds):
        leg_radius = 1
        dish_radius = 1
        current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
        current_pos_az = self.convertToCorrectRadians(current_position_data.leg_angle)
        current_pos_alt = current_position_data.dish_angle
        move_az = math.fabs(az - current_pos_az)
        move_alt = math.fabs(alt - current_pos_alt)
        print("moves: {}, {}".format(move_az, move_alt))
        leg_angular_velocity = move_az / seconds
        dish_angular_velocity = move_alt / seconds
        leg_linear_velocity = leg_radius * leg_angular_velocity
        dish_linear_velocity = dish_radius * dish_angular_velocity
        print("Leg velocity: {} m/s".format(leg_linear_velocity))
        print("Dish velocity: {} m/s".format(dish_linear_velocity))
        print("{{ leg_linear_velocity: {}, dish_linear_velocity: {} }}".format(leg_linear_velocity, dish_linear_velocity))

        self.publishCommand(leg_linear_velocity, dish_linear_velocity, az, alt)


    def makeMovement(self, az, alt, seconds):
        current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
        current_pos_az = self.convertToCorrectRadians(current_position_data.leg_angle)
        current_pos_alt = current_position_data.dish_angle
        displacement_az = math.fabs(az - current_pos_az)
        displacement_alt = math.fabs(alt - current_pos_alt)

        leg_acceleration = self.calcAcceleration(displacement_az, self.last_leg_joint_velocity, seconds, 1)
        dish_acceleration = self.calcAcceleration(displacement_alt, self.last_dish_joint_velocity, seconds, 1)
        self.last_leg_joint_velocity = self.calcVelocity2(self.last_leg_joint_velocity, 1, seconds, leg_acceleration)
        self.last_dish_joint_velocity = self.calcVelocity2(self.last_dish_joint_velocity, 1, seconds, dish_acceleration)
        print("POSITIONS: \n\tLEG: {}, {}\n\tDISH: {}, {}".format(az, current_pos_az, alt, current_pos_alt))
        print("ACCELERATIONS: \n\tLEG: {}\n\tDISH: {}".format(leg_acceleration, dish_acceleration))
        print("VELOCITIES: \n\tLEG: {}\n\tDISH: {}".format(self.last_leg_joint_velocity, self.last_dish_joint_velocity))


    def calcVelocity(self, angle, seconds, initial_velocity, radius, joint):
        current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
        current_position = 0
        if (joint == self.LEG_JOINT):
            current_position = self.convertToCorrectRadians(current_position_data.leg_angle)
        elif (joint == self.DISH_JOINT):
            current_position = current_position_data.dish_angle
        displacement = math.fabs(angle - current_position)
        acceleration = self.calcAcceleration(displacement, initial_velocity, seconds) * radius
        angular_velocity = ((2 * displacement) - (initial_velocity * seconds)) / seconds

    def calcVelocity2(self, initial_velocity, radius, seconds, acceleration):
        return (initial_velocity + acceleration * seconds) * radius

    def calcAcceleration(self, displacement, initial_velocity, seconds, radius):
        return (((2 * displacement) - (2 * initial_velocity * seconds)) / math.pow(seconds, 2)) * radius

    def publishCommand(self, leg_linear_velocity, dish_linear_velocity, leg_angle, dish_angle, leg_acceleration=0, dish_acceleration=0):
        # self.publish_command.publish(leg_linear_velocity=leg_linear_velocity, dish_linear_velocity=dish_linear_velocity)
        msg = Antenna_command()
        msg.leg_linear_velocity = leg_linear_velocity
        msg.dish_linear_velocity = dish_linear_velocity
        msg.leg_angle = leg_angle
        msg.dish_angle = dish_angle
        msg.leg_linear_acceleration = leg_acceleration
        msg.dish_linear_acceleration = dish_acceleration
        self.publish_command.publish(msg)

    def getNextPasses(self):
        self.max_elev_time = ""
        self.max_elev = 0
        lines = []
        for line in open('/home/rasmus/catkin_ws/src/antenna/antenna_controller/tle/tle.txt', 'r').readlines():
            lines.append(line)
        print("Get next passes tle: {}".format(lines))

        all_passes = []
        pass_parts = []
        obs = ephem.Observer()
        obs.lat = self.ground_station_latitude
        obs.long = self.ground_station_longitude
        obs.elevation = self.ground_station_elevation

        satellite = ephem.readtle(lines[0], lines[1], lines[2])
        satellite.compute(obs)

        while (len(pass_parts) == 0):
            pass_parts = []
            rise_time, rise_az, max_alt_time, max_alt, set_time, set_az = obs.next_pass(satellite)
            self.max_elev_time = max_alt_time
            self.max_elev = max_alt
            if (math.degrees(max_alt) < 0):
                obs.date = set_time + ephem.minute
                continue

            if (rise_time > set_time):
                range_s = satellite.range
                sat_az = math.degrees(satellite.az)
                sat_alt = math.degrees(satellite.alt)

                print("CURRENT PASS : rise_time: {}, set_time: {}, current_time: {}, range: {}, az: {}, alt: {}".format(rise_time, set_time, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), range_s, sat_az, sat_alt))

                turning_time = self.getTurningTime(sat_az, sat_alt)
                # loeb antenni asukohta ja arvutab, kaua aega l'heks antenni pooramiseni ja paneb selle aja rise_timele juurde.
                # See t'hendab, et kui programm naeb, et antenn ei joua kuidagi moodi isegi mootma hakata, siis ei hakka ta seda satelliiti
                # uldse jalgima.
                print("TURNING TIME : {} SECONDS".format(turning_time))

                rise_time = ephem.Date(ephem.Date(datetime.utcnow()) + ephem.second * (turning_time + 10))
                print("{}, | {}".format(rise_time, set_time))

                if (rise_time > set_time):
                    obs.date = set_time + ephem.minute
                    continue

            while (rise_time < set_time):
                obs.date = rise_time
                satellite.compute(obs)
                pass_parts.append((rise_time, math.radians(math.degrees(satellite.alt)), math.radians(math.degrees(satellite.az)), lines[0], int(lines[2].split(" ")[1])))
                rise_time = ephem.Date(rise_time + ephem.second * self.seconds_per_move)
            # obs.date = rise_time + ephem.minute

        print("ALL PASSES LENGTH: {}".format(len(all_passes)))
        self.next_pass = pass_parts

    def getTurningTime(self, sat_az, sat_alt):
        current_position_data = rospy.wait_for_message('/antenna/antenna_position', Antenna_position)
        current_pos_az = self.convertToCorrectRadians(current_position_data.leg_angle)
        current_pos_alt = current_position_data.dish_angle
        # current_pos_az = self.convertToCorrectRadians(rospy.wait_for_message('/antenna/leg_joint_position_controller/state', JointControllerState).set_point)
        # current_pos_alt = rospy.wait_for_message('/antenna/dish_joint_position_controller/state', JointControllerState).set_point
        dish_joint_time = math.fabs(sat_alt - math.degrees(current_pos_alt)) / self.max_dish_joint_angular_velocity
        leg_joint_time = math.fabs(sat_az - math.degrees(current_pos_az)) / self.max_leg_joint_angular_velocity
        if (dish_joint_time > leg_joint_time):
            return dish_joint_time
        else:
            return leg_joint_time

    def changeAntennaState(self):
        if (self.is_stopped):
            self.is_stopped = False
            rospy.loginfo("Shut down antenna")
        else:
            self.is_stopped = True
            rospy.loginfo("Continue tracking")


def main():
    controller = SatelliteTracker()
    controller.runProgram()

    # p = multiprocessing.Process(target=tleSchedule)
    # p.start()

    # d = multiprocessing.Process(target=runProgram)
    # d.start()

    # Kui anda ette satelliit, mis vaatev'lja kunagi ei joua, siis error  +
    # Sujuv liikumine. URDF korda Vaadata mis pidi liikus eelmine kord ja siis liikuda vastupidi
    # Min horizon - Vist tootab, aga kontrolli ule. Lisaks vaja kontrollida satelliitide ulelennu ajad. Tundub, et horizoni panemisega annabki ta ulelennu vastavast horizonis horizonini. Meie tahame, et ta lihtsalt skipiks need, mis ule mingi horizoni kunagi ei joua, aga hakkaks neid jalgima ikkagi nullist. For, if
    # Kui gazebo ei toota +
    # Kui satelliiti j'lgima hakates on satelliit juba vaatevaljas
    # print("%s | %4.1f %5.1f | %4.1f %+6.1f | %5.1f" % \
    #              (rise_time,
    #                  math.degrees(satellite.alt),
    #                  math.degrees(satellite.az),
    #                  math.degrees(satellite.sublat),
    #                  math.degrees(satellite.sublong),
    #                  satellite.elevation/1000.))

    # Kui satelliit on juba pea kohal, siis peaks samuti hakkama seda jälgima. Siin aga võiks arvestada ka olukorraga, kus antenn
    # ei jõuaks nagunii satelliidini vajaliku aja jooksul liikuda. Sellisel juhul poleks sellest hetke asukoha jälgimisest suurt kasu
    # ning antenn peaks liikuma järgmise alguspunkti peale. Seda tehes peab arvestama antenni võimaliku max kiirusega liigutamisel
    # õigesse kohta kuluvat aega.

    # Kui algselt tööle panna, siis ei peaks ta alati samale poole minema, vaid vaatama hetke asukoha järgi, kummale poole mõislikum liikuda on.
    # Üldiselt pean rohkem kontrollima antenni hetke asukohta ja selle abil otsustama, kummale poole liikuda. Ilmselt suurem osa
    # ajast saan kasutada sama loogikat, et liigu vastupidi eelmisele, kuid on olukordi, mil see viis ei tööta ja antenn võib
    # hakata potentsiaalselt liikuma praktiliselt ringiratast.  - Ei saa enne teha, kui tean reaalset antenni andmeid

    # Teha tle küsimine sagedasemaks. Nt, iga paari tunni tagant +

    # Mida teha taldrikuga. Hetkel on ulemine asend 0 ja vahemik on -pi/2 - +pi/2. Siiamaani teinud nii, et lahutan pi/2, aga nii saan
    # alati ainult [hele poole liikuda ?

    # Seniidis - 1-3 h

    # Refactor - Loo mingi osa funktsioone lahku - 1h


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
