#!/usr/bin/env python

from antenna_msgs.msg import Weather_information
import rospy
import json
import urllib2
import schedule
import time


class WeatherController():
    """docstring for WeatherController"""
    def __init__(self):
        self.API_URL = ""
        self.publish_command = rospy.Publisher("/antenna/weather_information", Weather_information, queue_size=10)

    def weatherSchedule(self):
        rospy.init_node('weather_information')
        self.API_URL = self.getApiUrl()
        self.trackWeather()

        schedule.every(10).seconds.do(self.trackWeather)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def trackWeather(self):
        weather_data = self.getWeatherData()
        wind_direction = weather_data['wind_deg']
        if (wind_direction is None):
            wind_direction = 0
        antenna_direction = self.calculateAntennaDirection(wind_direction)
        dt = weather_data['dt']
        wind_speed = weather_data['wind']
        should_stop_antenna = False
        if (wind_speed >= 10):
            should_stop_antenna = True
        self.publishCommand(should_stop_antenna, wind_speed, wind_direction, antenna_direction, 4, dt)

    def publishCommand(self, should_stop_antenna, wind_speed, wind_direction, antenna_az, antenna_el, dt):
        tst = {"should_stop_antenna": should_stop_antenna,
               "wind_speed": wind_speed,
               "wind_direction": wind_direction,
               "antenna_az": antenna_az,
               "antenna_el": antenna_el,
               "dt": dt}
        rospy.set_param('weather_information', tst)
        msg = Weather_information()
        msg.should_stop_antenna = should_stop_antenna
        msg.avg_wind_speed = wind_speed
        msg.wind_direction = wind_direction
        msg.antenna_stop_azimuth = antenna_az
        msg.antenna_stop_elevation = antenna_el
        msg.date_time = dt
        self.publish_command.publish(msg)

    def calculateAntennaDirection(self, wind_direction):
        return (wind_direction + 90) % 360

    def getWeatherData(self):
        request = urllib2.Request(self.API_URL)
        response = urllib2.urlopen(request)
        # url = urllib2.request.urlopen(self.API_URL)
        output = response.read().decode('utf-8')
        data = json.loads(output)
        # print(data)
        data = self.getFormattedData(data)
        print(data)
        return data

    def getFormattedData(self, data):
        # formatted_data = dict(
        #     city=data.get('name'),
        #     country=data.get('sys').get('country'),
        #     temp=data.get('main').get('temp'),
        #     temp_max=data.get('main').get('temp_max'),
        #     temp_min=data.get('main').get('temp_min'),
        #     humidity=data.get('main').get('humidity'),
        #     pressure=data.get('main').get('pressure'),
        #     sky=data['weather'][0]['main'],
        #     sunrise=data.get('sys').get('sunrise'),
        #     sunset=data.get('sys').get('sunset'),
        #     wind=data.get('wind').get('speed'),
        #     wind_deg=data.get('wind').get('deg'),
        #     dt=data.get('dt'),
        #     cloudiness=data.get('clouds').get('all'),
        # )

        first_prediction = data.get('list')[0]
        formatted_data = dict(
            city=data.get('city').get('name'),
            country=data.get('city').get('country'),
            wind=first_prediction.get('wind').get('speed'),
            wind_deg=first_prediction.get('wind').get('deg'),
            dt_txt=first_prediction.get('dt_txt'),
            dt=first_prediction.get('dt')
        )
        return formatted_data

    def getApiUrl(self):
        latitude = '59.394870'
        longitude = '24.661399'
        api_key = 'c82cf06f9f08cb91929635b916ee19b6'
        # url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(latitude, longitude, api_key)
        url = 'http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'.format(latitude, longitude, api_key)
        return url


if __name__ == '__main__':
    WeatherController().weatherSchedule()
    # WeatherController().getWeatherData()
    # SatelliteChooser().chooseSatellite()
