#!/usr/bin/python
# OpenWeather using Python
from __future__ import print_function
"""
Usage: Python-OpenWeather.py
Makes API calls to OpenWeather and retrievs JSON data
Parses JSON data using JSON library
_______
-h or help  Displays this message
"""

import urllib
import json
import codecs
import gzip
import time
#from urllib.parse import urlencode for Python3
#import urllib.request for Python3


from sys import argv, exit

if len(argv) > 1:
    print(__doc__)
    exit(0)

locationID = 2911964
apikey = '4018963b8a12ea4aafa4b61cebcb9f8a'
serviceUrl = "http://api.openweathermap.org/data/2.5/weather?"
# url = serviceUrl + urllib.parse.urlencode({'id': locationID, 'APPID': apikey})
# urlRead = urllib.request.urlopen(url).read()
url = serviceUrl + urllib.urlencode({'id': locationID, 'APPID': apikey})
urlRead = urllib.urlopen(url).read()

dataJSON = json.loads(urlRead)

dt = float(dataJSON["dt"])
dt_local = time.time()
temp = float(dataJSON['main']['temp']) - 273.0
tempMax = float(dataJSON['main']['temp_max']) - 273.0
tempMin = float(dataJSON['main']['temp_min']) - 273.0
humidity = int(dataJSON['main']['humidity'])
pressure = int(dataJSON['main']['pressure'])
wind = dataJSON['wind']
windSpeed = float(dataJSON['wind']['speed'])
windDeg = float(dataJSON['wind']['deg'])
condition = dataJSON['weather'][0]['description']
clouds = int(dataJSON['clouds']['all'])
print("")
print("*******************")
print("--Weather Summary--")
print("*******************")
print("dt "+str(dt))
print("dt_local " + str(dt_local))
print("GMT "+ str(time.asctime(time.gmtime(dt))))
print("LOCAL" + time.ctime(dt))
print("CURRENT "+ time.ctime(dt_local))

print("Current Temperature: %.2f C" % temp)
print("Maximum Temperature: %.2f C" % tempMax)
print("Minimum Temperature: %.2f C" % tempMin)
print("Pressure: %d hpa" % pressure)
print("Humidity: %d %%" % humidity)
if 'gust' in wind:
    windGust = float(dataJSON['wind']['gust'])
    print("Wind Gust:%s m/s" % windGust)
else:
    print("Wind Gust: Data not available")

print("Wind Speed: %.2f m/s" % windSpeed)
print("Wind Deg: %.2f Degree" % windDeg)
print("Clouds: %d %%" % clouds)
print("Condition: %s" % condition)