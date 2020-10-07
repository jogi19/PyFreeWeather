#!/usr/bin/python
# OpenWeather using Python
from __future__ import print_function
from time import timezone
"""
Usage: Python-OpenWeather.py
Makes API calls to OpenWeather and retrievs JSON data
Parses JSON data using JSON library
_______
-h or help  Displays this message
"""

import urllib
import urllib.parse
import urllib.request
import json
import codecs
import gzip
import time
import sqlite3
#from urllib.parse import urlencode for Python3
#import urllib.request for Python3
from sys import argv, exit

if len(argv) > 1:
    print(__doc__)
    exit(0)


class OpenWeatherReceiver():
    locationID = 2911964
    apikey = '4018963b8a12ea4aafa4b61cebcb9f8a'

    """
    This class needs to be implemented
    """
    def __init__(self, locationID = 2911964, apikey = '4018963b8a12ea4aafa4b61cebcb9f8a'):
        """
        docstring
        """
        self.locationID = locationID
        self.apikey = apikey

    def retrievWeatherData(self):
        self.serviceUrl = "http://api.openweathermap.org/data/2.5/weather?"
        url = self.serviceUrl + urllib.parse.urlencode({'id': self.locationID, 'APPID': self.apikey})
        urlRead = urllib.request.urlopen(url).read()
        dataJSON = json.loads(urlRead)

        # coord #
        self.coord__lon = float(dataJSON['coord']['lon'])
        self.coord__lon = float(dataJSON['coord']['lat'])
        # weaher
        self.weather_id = dataJSON['weather'][0]['id']
        self.weather_main = dataJSON['weather'][0]['main']
        self.weather_description = dataJSON['weather'][0]['description']
        self.weather_icon = dataJSON['weather'][0]['icon']

        # base #
        self.base = dataJSON['base']

        # main #
        self.main_temp = float(dataJSON['main']['temp'])
        self.main_pressure = float(dataJSON['main']['pressure'])
        self.main_humidity = float(dataJSON['main']['humidity'])
        self.main_temp_min = float(dataJSON['main']['temp_min'])
        self.main_temp_max = float(dataJSON['main']['temp_max'])

        # wind #
        self.wind = dataJSON['wind']
        self.wind_speed = float(dataJSON['wind']['speed'])
        self.wind_deg = float(dataJSON['wind']['deg'])
        if 'gust' in self.wind:
            self.wind_gust = float(dataJSON['wind']['gust'])

        # clouds #
        self.clouds_all = dataJSON['clouds']['all']

        # dt#
        self.dt = float(dataJSON["dt"])

        # sys #
        self.sys_type = dataJSON['sys']['type']
        self.sys_id = dataJSON['sys']['id']
        # sys_message = dataJSON['sys']['message'] //KeyError 'message'
        self.sys_country = dataJSON['sys']['country']
        self.sys_sunrise = dataJSON['sys']['sunrise']
        self.sys_sunset = dataJSON['sys']['sunset']
        self.sys_timezone = dataJSON['timezone']

        self.dt = float(dataJSON["dt"])
        self.dt_local = time.time()
        self.main = dataJSON
        self.temp = float(dataJSON['main']['temp']) - 273.0
        self.tempMax = float(dataJSON['main']['temp_max']) - 273.0
        self.tempMin = float(dataJSON['main']['temp_min']) - 273.0
        self.tempFeelsLike = float(dataJSON['main']['feels_like']) - 273.0
        self.humidity = int(dataJSON['main']['humidity'])
        self.pressure = int(dataJSON['main']['pressure'])
        self.wind = dataJSON['wind']
        self.name = dataJSON['name']
        self.windSpeed = float(dataJSON['wind']['speed'])
        self.windDeg = float(dataJSON['wind']['deg'])
        self.condition = dataJSON['weather'][0]['description']
        self.clouds = int(dataJSON['clouds']['all'])
        self.visibility = int(dataJSON['visibility'])

    def printWeatherData(self):
        print("*******************")
        print("--Weather Summary--")
        print("*******************")
        print("Name "+self.name)
        print("base "+self.base)
        print("dt "+str(self.dt))
        print("GMT "+ str(time.asctime(time.gmtime(self.dt))))
        print("Timezone "+str(self.sys_timezone))
        print("LOCAL " + time.ctime(self.dt))
        print("CURRENT "+ time.ctime(self.dt_local))
        print("Sunrise GMT "+ str(time.asctime(time.gmtime(self.sys_sunrise))))
        print("Sunset GMT "+ str(time.asctime(time.gmtime(self.sys_sunset))))

        print("Current Temperature: %.2f C" % self.temp)
        print("Maximum Temperature: %.2f C" % self.tempMax)
        print("Minimum Temperature: %.2f C" % self.tempMin)
        print("Feels Like Temperatur: %.2f C" % self.tempFeelsLike)
        print("Pressure: %d hpa" % self.pressure)
        print("Humidity: %d %%" % self.humidity)
        if 'gust' in self.wind:
            self.windGust = float(dataJSON['wind']['gust'])
            print("Wind Gust:%s m/s" % self.windGust)
        else:
            print("Wind Gust: Data not available")

        print("Wind Speed: %.2f m/s " % self.windSpeed)
        print("Wind Deg: %.2f Degree" % self.windDeg)
        print("Clouds: %d %%" % self.clouds)
        print("Condition: %s" % self.condition)
        print("visibility: %s m" % str(self.visibility))


fw = OpenWeatherReceiver(2911964, '4018963b8a12ea4aafa4b61cebcb9f8a')
fw.retrievWeatherData()
fw.printWeatherData()