#!/usr/bin/python
# OpenWeather using Python
from __future__ import print_function
import urllib
import urllib.parse
import urllib.request
from time import timezone
"""
Usage: Python-OpenWeather.py
Makes API calls to OpenWeather and retrievs JSON data
Parses JSON data using JSON library
_______
-h or help  Displays this message
"""


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
    def __init__(self, locationID, apikey):
        """
        docstring
        """
        self.locationID = locationID
        self.apikey = apikey

    def retrievWeatherData(self):
        self.serviceUrl = "http://api.openweathermap.org/data/2.5/weather?"
        url = self.serviceUrl + urllib.parse.urlencode(
            {'id': self.locationID, 'APPID': self.apikey})
        urlRead = urllib.request.urlopen(url).read()
        print(urlRead)
        dataJSON = json.loads(urlRead)

        # coord #
        self.coord_lon = float(dataJSON['coord']['lon'])
        self.coord_lat = float(dataJSON['coord']['lat'])
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
        else:
            self.wind_gust = None

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
        self.main_temp = float(dataJSON['main']['temp']) - 273.0
        self.main_tempMax = float(dataJSON['main']['temp_max']) - 273.0
        self.main_tempMin = float(dataJSON['main']['temp_min']) - 273.0
        self.main_temp_feels_like = float(dataJSON['main']['feels_like']) - 273.0
        self.main_humidity = int(dataJSON['main']['humidity'])
        self.main_pressure = int(dataJSON['main']['pressure'])
        self.wind = dataJSON['wind']
        if 'gust' in self.wind:
            self.wind_gust = float(dataJSON['wind']['gust'])
        else:
            self.wind_gust = None
        self.windSpeed = float(dataJSON['wind']['speed'])
        self.windDeg = float(dataJSON['wind']['deg'])
        self.condition = dataJSON['weather'][0]['description']
        self.clouds = int(dataJSON['clouds']['all'])
        self.visibility = int(dataJSON['visibility'])

        self.name = dataJSON['name']

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
        print("self.coord_lon: "+ (str(self.coord_lon)))
        print("self.coord_lat: "+ (str(self.coord_lat)))
        print("Sunrise GMT "+ str(time.asctime(time.gmtime(self.sys_sunrise))))
        print("Sunset GMT "+ str(time.asctime(time.gmtime(self.sys_sunset))))

        print("Current Temperature: %.2f C" % self.main_temp)
        print("Maximum Temperature: %.2f C" % self.main_tempMax)
        print("Minimum Temperature: %.2f C" % self.main_tempMin)
        print("Feels Like Temperatur: %.2f C" % self.main_temp_feels_like)
        print("Pressure: %d hpa" % self.main_pressure)
        print("Humidity: %d %%" % self.main_humidity)
        print("Wind Gust:%s m/s" % self.wind_gust)
        
        print("Wind Speed: %.2f m/s " % self.windSpeed)
        print("Wind Deg: %.2f Degree" % self.windDeg)
        print("Clouds All: %d %%" % self.clouds_all)
        print("Clouds: %d %%" % self.clouds)
        print("Condition: %s" % self.condition)
        print("self.weather_main "+str(self.weather_main))
        print("visibility: %s m" % str(self.visibility))

    '''
    coord
    '''
    def get_coord_lon(self):
        '''
        City geo location, longitude
        '''
        return self.coord_lon

    def get_coord_lat(self):
        '''
        City geo location, latitude
        '''
        return self.coord_lat

    '''
    weather
    '''
    def get_weather_id(self):
        '''
        Weather condition id
        '''
        return self.weather_id

    def get_weather_main(self):
        '''
        Group of weather parameters (Rain, Snow, Extreme etc.)
        '''
        return self.weather_main

    def get_weather_description(self):
        '''
        Weather condition within the group. You can get the output in your language.
        '''
        return self.weather_description

    '''
    base    
    '''
    def get_base(self):
        '''
        Internal parameter
        '''
        return self.base

    '''
    main
    '''
    def get_main_temp(self):
        '''
        Temperature. Unit Default: Kelvin, Metric: Celsius,
        Imperial: Fahrenheit.
        '''
        return self.main_temp

    def get_main_feels_like(self):
        '''
        Temperature. This temperature parameter accounts
        for the human perception of weather. 
        Unit Default: 
        Kelvin, Metric: Celsius, Imperial: Fahrenheit. 
        '''
        return self.main_temp_feels_like

    def get_main_pressure(self):
        '''
        Atmospheric pressure (on the sea level, if there is no sea_level or grnd_level data), hPa
        '''
        return self.main_pressure

    def get_humidity(self):
        '''
        Humidity, %
        '''
        return self.main_humidity

    def get_temp_min(self):
        '''
        Minimum temperature at the moment.
        This is minimal currently observed temperature
        (within large megalopolises and urban areas).
        Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
        '''
        return self.main_temp_min

    def get_main_temp_max(self):
        '''
        Maximum temperature at the moment.
        This is maximal currently observed temperature
        (within large megalopolises and urban areas).
        Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit.
        '''
        return self.main_temp_max

    def get_main_sea_level(self):
        '''
        Atmospheric pressure on the sea level, hPa
        NOT IMPLEMENTED
        '''
        return None

    def get_main_grnd_level(self):
        '''
        Atmospheric pressure on the ground level, hPa
        NOT IMPLEMENTED
        '''
        return None

    '''
    wind
    '''





fw = OpenWeatherReceiver(2911964, '4018963b8a12ea4aafa4b61cebcb9f8a')
fw.retrievWeatherData()
fw.printWeatherData()
