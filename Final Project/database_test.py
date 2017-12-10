import sqlite3


conn = sqlite3.connect("country_weather_db.sqlite")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS WEATHER")
cur.execute('CREATE TABLE WEATHER (city TEXT NOT NULL PRIMARY KEY UNIQUE, temp INTEGER, data DATETIME)')