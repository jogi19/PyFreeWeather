'''
source: https://www.w3schools.com/python/python_mysql_getstarted.asp
This code was just to leran how to handle SQL data base with python
and helped me to create the required databases and tables
I'm not sure if this version creates the correct databases
So, if you find issues, don't hessitate to push fixes :-)
'''

import mysql.connector

def create_database(database):
  mycursor.execute("CREATE DATABASE " + database)

def show_databases():
  mycursor.execute("SHOW DATABASES")
  for x in mycursor:
    print(x)

def create_table(database, table):
  mydb.database = database
  mycursor.execute("CREATE TABLE "+ table+"(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

def create_weather_table(database, table):
  mydb.database = database
  sql = "CREATE TABLE "+ table+"( time DATETIME NOT NULL,\
    local_time DATETIME,\
    timezone INT,\
    sys_sunrise DATETIME,\
    sys_sunset DATETIME,\
    coord_lon FLOAT,\
    coord_lat FLOAT,\
    weather_id INT,\
    weather_main CHAR(64),\
    weather_description CHAR(64),\
    base CHAR(64),\
    wind_speed FLOAT,\
    wind_deg FLOAT,\
    wind_gust FLOAT,\
    sys_type INT,\
    main_temp FLOAT,\
    main_temp_max FLOAT,\
    main_temp_min FLOAT,\
    main_temp_feels_like FLOAT,\
    main_humidity INT,\
    main_pressure INT,\
    clouds_all INT,\
    visibility INT,\
    id INT,\
    name CHAR(128))"
  print(sql)
  mycursor.execute(sql)



   
def alter_table(database, table):
  mydb.database = database
  mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY") 

mydb = mysql.connector.connect(
  host="localhost",
  user="weatherfrog",
  password="forecast"
)
mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")
show_databases()
create_weather_table("weather_db","weather_test5")

