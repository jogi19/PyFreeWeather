'''
source: https://www.w3schools.com/python/python_mysql_getstarted.asp
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
#create_table("mydatabase","weather")

