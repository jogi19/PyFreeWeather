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
import time
import mysql.connector
import datetime
import pytz
from sys import argv, exit
import paho.mqtt.client as mqtt

class OpenWeatherReceiver():

    """
    TODO Decription of class
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
            self.wind_gust = self.wind_speed

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
        self.timezone = dataJSON['timezone']

        self.dt = float(dataJSON["dt"])
        self.dt_current = time.time()
        #self.main = dataJSON //is this need ?
        #TODO store temp in Celvin not Celcius
        self.main_temp = float(dataJSON['main']['temp'])
        self.main_tempMax = float(dataJSON['main']['temp_max'])
        self.main_tempMin = float(dataJSON['main']['temp_min'])
        self.main_temp_feels_like = float(dataJSON['main']['feels_like'])
        self.main_humidity = int(dataJSON['main']['humidity'])
        self.main_pressure = int(dataJSON['main']['pressure'])

        self.weather_description = dataJSON['weather'][0]['description']
        self.clouds = int(dataJSON['clouds']['all'])
        self.visibility = int(dataJSON['visibility'])
        self.id = dataJSON['id']
        self.name = dataJSON['name']
        #self.code = dataJSON['code']

    def printWeatherData(self):
        print("*******************")
        print("--Weather Summary--")
        print("*******************")
        print("Name "+self.get_name())
        print("base "+self.get_base())
        print("dt "+str(self.get_dt()))
        #time_string = str(time.asctime(time.gmtime(self.get_dt())))
        timestamp = datetime.datetime.fromtimestamp(self.get_dt()).strftime('%Y-%m-%d %H:%M:%S')
        time_string = str(time.gmtime(self.get_dt()))
        print("GMT "+ timestamp)

        print("Timezone "+str(self.get_timezone()))
        print("LOCAL " + time.ctime(self.get_dt()))
        print("LOCAL " + str(time.asctime(time.gmtime(self.get_dt()+self.get_timezone()))))
        print("CURRENT "+ time.ctime(self.get_dt_current()))
        print("self.coord_lon: "+ (str(self.get_coord_lon())))
        print("self.coord_lat: "+ (str(self.get_coord_lat())))
        print("Sunrise GMT "+ str(time.asctime(time.gmtime(self.get_sys_sunrise()))))
        print("Sunset GMT "+ str(time.asctime(time.gmtime(self.get_sys_sunset()))))

        print("Current Temperature: %.2f C" % self.get_main_temp())
        print("Maximum Temperature: %.2f C" % self.get_main_temp_max())
        print("Minimum Temperature: %.2f C" % self.get_main_temp_min())
        print("Feels Like Temperatur: %.2f C" % self.get_main_temp_feels_like())
        print("Pressure: %d hpa" % self.get_main_pressure())
        print("Humidity: %d %%" % self.get_main_humidity())
        print("Wind Gust:%s m/s" % self.get_wind_gust())
        
        print("Wind Speed: %.2f m/s " % self.get_wind_speed())
        print("Wind Deg: %.2f Degree" % self.get_wind_deg())
        print("Clouds All: %d %%" % self.get_clouds_all())
        print("Clouds: %d %%" % self.get_clouds_all())
        print("weather_description: %s" % self.get_weather_description())
        print("self.weather_main "+str(self.get_weather_main()))
        print("visibility: %s m" % str(self.get_visibility()))

    def insert_weather_data(self, database, table):
        mydb = mysql.connector.connect(
          host="localhost",
          user="weatherfrog",
          password="forecast"
        )
        mydb.database = database
        mycursor = mydb.cursor()
        sql = "INSERT INTO " +table+ "(\
        time,\
        local_time,\
        timezone,\
        sys_sunrise,\
        sys_sunset,\
        coord_lon,\
        coord_lat,\
        weather_id,\
        weather_main,\
        weather_description,\
        base,\
        wind_speed,\
        wind_deg,\
        wind_gust,\
        sys_type,\
        main_temp,\
        main_temp_max,\
        main_temp_min,\
        main_temp_feels_like,\
        main_humidity,\
        main_pressure,\
        clouds_all,\
        visibility,\
        id,\
        name)\
         VALUES \
        ( \
        \'"+str(datetime.datetime.fromtimestamp(self.get_dt(),tz=pytz.utc).strftime('%Y-%m-%d %H:%M:%S'))+"\',\
        \'"+str(datetime.datetime.fromtimestamp(self.get_dt()).strftime('%Y-%m-%d %H:%M:%S'))+"\',\
        "+str(self.get_timezone())+",\
        \'"+str(datetime.datetime.fromtimestamp(self.get_sys_sunrise(),tz=pytz.utc).strftime('%Y-%m-%d %H:%M:%S'))+"\',\
        \'"+str(datetime.datetime.fromtimestamp(self.get_sys_sunset(),tz=pytz.utc).strftime('%Y-%m-%d %H:%M:%S'))+"\',\
        "+str(self.get_coord_lon())+",\
        "+str(self.get_coord_lat())+",\
        "+str(self.get_weather_id())+",\
        \'"+str(self.get_weather_main())+"\',\
        \'"+self.get_weather_description()+"\',\
        \'"+str(self.get_base())+"\',\
        "+str(self.get_wind_speed())+",\
        "+str(self.get_wind_deg())+",\
        "+str(self.get_wind_gust())+",\
        "+str(self.get_sys_type())+",\
        "+str(self.get_main_temp())+",\
        "+str(self.get_main_temp_max())+",\
        "+str(self.get_main_temp_min())+",\
        "+str(self.get_main_temp_feels_like())+",\
        "+str(self.get_main_humidity())+",\
        "+str(self.get_main_pressure())+",\
        "+str(self.get_clouds_all())+",\
        "+str(self.get_visibility())+",\
        "+str(self.get_id())+",\
        \'"+self.get_name()+"\');"
        print(sql)
        mycursor.execute(sql)
        mydb.commit()


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

    def get_main_temp_feels_like(self):
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

    def get_main_humidity(self):
        '''
        Humidity, %
        '''
        return self.main_humidity

    def get_main_temp_min(self):
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

    def get_wind_speed(self):
        '''
         Wind speed. Unit Default: meter/sec, Metric: meter/sec, Imperial: miles/hour.
        '''
        return self.wind_speed

    def get_wind_deg(self):
        '''
        Wind direction, degrees (meteorological)
        '''
        return self.wind_deg

    def get_wind_gust(self):
        '''
        Wind gust. Unit Default: meter/sec, Metric: meter/sec, Imperial: 
        '''
        return self.wind_gust

    '''
    clouds
    '''
    def get_clouds_all(self):
        '''
        Cloudiness, %
        '''
        return self.clouds_all

    '''
    visibility
    '''
    def get_visibility(self):
        '''
        Visibility, meter
        '''
        return self.visibility
    '''
    dt
    '''
    def get_dt(self):
        '''
        Time of data calculation, unix, UTC 
        '''
        return self.dt

    '''
    df current
    '''
    def get_dt_current(self):
        '''
        Time of data retrieving, unit, UTC
        '''
        return self.dt_current

    '''
    sys
    '''
    def get_sys_type(self):
        '''
        Internal parameter
        '''
        return self.sys_type

    def get_sys_id(self):
        '''
        Internal parameter
        '''
        return self.sys_id

    def get_sys_message(self):
        '''
        Internal parameter
        NOT IMPLEMENTED
        '''
        return None

    def get_sys_country(self):
        '''
        Country code (GB, JP etc.)
        '''
        return self.sys_country

    def get_sys_sunrise(self):
        '''
        Sunrise time, unix, UTC
        '''
        return self.sys_sunrise

    def get_sys_sunset(self):
        '''
        Sunset time, unix, UTC
        '''
        return self.sys_sunset

    '''
    timezone
    '''
    def get_timezone(self):
        '''
        Shift in seconds from UTC 
        '''
        return self.timezone

    '''
    id
    '''
    def get_id(self):
        '''
        City ID
        '''
        return self.id

    '''
    name
    '''
    def get_name(self):
        '''
        City name 
        '''
        return self.name

    '''
    cod
    '''
    def get_code(self):
        '''
            Internal parameter
            NOT IMPLEMENTED
        '''
        return None

    def publish_MQTT(self):
        mqttBroker="192.168.178.119"
        client = mqtt.Client("WeatherStation_Haiger")
        client.connect(mqttBroker)
        client.publish("WEATHERSTATION/HAIGER/TEMPERATUR/FEELS_LIKE/",self.get_main_temp_feels_like())
        time.sleep(1)
        client.publish("WEATHERSTATION/HAIGER/TEMPERATUR/MAIN/",self.get_main_temp())
        time.sleep(1)
        client.publish("WEATHERSTATION/HAIGER/TEMPERATUR/MAX/",self.get_main_temp_max())
        client.publish("WEATHERSTATION/HAIGER/TEMPERATUR/MIN/",self.get_main_temp_min())
        client.publish("WEATHERSTATION/HAIGER/WIND/DIRECTION/",self.get_wind_deg())
        client.publish("WEATHERSTATION/HAIGER/WIND/SPEED/",self.get_wind_speed())
        client.publish("WEATHERSTATION/HAIGER/WIND/GUST/",self.get_wind_gust())
        client.publish("WEATHERSTATION/HAIGER/CLOUDS/",self.get_clouds_all())
        client.publish("WEATHERSTATION/HAIGER/PRESSURE/",self.get_main_pressure())
        client.publish("WEATHERSTATION/HAIGER/HUMIDITY/",self.get_main_humidity())
        client.publish("WEATHERSTATION/HAIGER/WEATHER_DESCRIPTION/",self.get_weather_description())
        client.publish("WEATHERSTATION/HAIGER/WEATHER_MAIN/",self.get_weather_main())


if len(argv) < 1:
    exit()


locationID=int(argv[1])
print(locationID)
apikey=str(argv[2])
print(apikey)
fw = OpenWeatherReceiver(locationID, apikey)
fw.retrievWeatherData()
fw.printWeatherData()

fw.insert_weather_data("weather_db","weather_test5")
fw.publish_MQTT()
