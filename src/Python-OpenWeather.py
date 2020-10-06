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

    
locationID = 2911964
apikey = '4018963b8a12ea4aafa4b61cebcb9f8a'
serviceUrl = "http://api.openweathermap.org/data/2.5/weather?"

#Python 3
url = serviceUrl + urllib.parse.urlencode({'id': locationID, 'APPID': apikey})
urlRead = urllib.request.urlopen(url).read()

#Python 2
#url = serviceUrl + urllib.urlencode({'id': locationID, 'APPID': apikey})
#urlRead = urllib.urlopen(url).read()
# API response info https://openweathermap.org/current
dataJSON = json.loads(urlRead)

# coord #
coord__lon = float(dataJSON['coord']['lon'])
coord__lon = float(dataJSON['coord']['lat'])
# weaher
weather_id = dataJSON['weather'][0]['id']
weather_main = dataJSON['weather'][0]['main']
weather_description = dataJSON['weather'][0]['description']
weather_icon = dataJSON['weather'][0]['icon']

# base #
base = dataJSON['base']

# main #
main_temp = float(dataJSON['main']['temp'])
main_pressure = float(dataJSON['main']['pressure'])
main_humidity = float(dataJSON['main']['humidity'])
main_temp_min = float(dataJSON['main']['temp_min'])
main_temp_max = float(dataJSON['main']['temp_max'])

# wind #
wind = dataJSON['wind']
wind_speed = float(dataJSON['wind']['speed'])
wind_deg = float(dataJSON['wind']['deg'])
if 'gust' in wind:
    wind_gust = float(dataJSON['wind']['gust'])

# clouds #
clouds_all = dataJSON['clouds']['all']

# dt#
dt = float(dataJSON["dt"])

# sys #
sys_type = dataJSON['sys']['type']
sys_id = dataJSON['sys']['id']
# sys_message = dataJSON['sys']['message'] //KeyError 'message'
sys_country = dataJSON['sys']['country']
sys_sunrise = dataJSON['sys']['sunrise']
sys_sunset = dataJSON['sys']['sunset']
sys_timezone = dataJSON['timezone']
sys_id = dataJSON['sys']['id']
#sys_name = dataJSON['sys']['name']
#sys_cod = dataJSON['sys']['cod']

# conn = sqlite3.connect("openweather.db")
# c = conn.cursor()
# my_data = (dt, main_temp, main_pressure, main_humidity, main_temp_min, main_temp_max)
# c.execute('INSERT INTO main VALUES (? ? ? ? ? ?)', my_data)
# conn.commit()

##########################
print(dataJSON)
dt = float(dataJSON["dt"])
dt_local = time.time()
main = dataJSON
temp = float(dataJSON['main']['temp']) - 273.0
tempMax = float(dataJSON['main']['temp_max']) - 273.0
tempMin = float(dataJSON['main']['temp_min']) - 273.0
tempFeelsLike = float(dataJSON['main']['feels_like']) - 273.0
humidity = int(dataJSON['main']['humidity'])
pressure = int(dataJSON['main']['pressure'])
wind = dataJSON['wind']
name = dataJSON['name']
windSpeed = float(dataJSON['wind']['speed'])
windDeg = float(dataJSON['wind']['deg'])
condition = dataJSON['weather'][0]['description']
clouds = int(dataJSON['clouds']['all'])
visibility = int(dataJSON['visibility'])
print("urlRead "+ urlRead)
print("*******************")
print("--Weather Summary--")
print("*******************")
print("Name "+name)
print("base "+base)
print("dt "+str(dt))
print("GMT "+ str(time.asctime(time.gmtime(dt))))
print("Timezone "+str(timezone))
print("LOCAL " + time.ctime(dt))
print("CURRENT "+ time.ctime(dt_local))
print("Sunrise GMT "+ str(time.asctime(time.gmtime(sys_sunrise))))
print("Sunset GMT "+ str(time.asctime(time.gmtime(sys_sunset))))

print("Current Temperature: %.2f C" % temp)
print("Maximum Temperature: %.2f C" % tempMax)
print("Minimum Temperature: %.2f C" % tempMin)
print("Feels Like Temperatur: %.2f C" % tempFeelsLike)
print("Pressure: %d hpa" % pressure)
print("Humidity: %d %%" % humidity)
if 'gust' in wind:
    windGust = float(dataJSON['wind']['gust'])
    print("Wind Gust:%s m/s" % windGust)
else:
    print("Wind Gust: Data not available")

print("Wind Speed: %.2f m/s " % windSpeed)
print("Wind Deg: %.2f Degree" % windDeg)
print("Clouds: %d %%" % clouds)
print("Condition: %s" % condition)
print("visibility: %s m" % str(visibility))