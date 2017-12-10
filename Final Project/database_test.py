import sqlite3


conn = sqlite3.connect("state_weather_db.sqlite")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS WEATHER")
cur.execute('CREATE TABLE WEATHER (city TEXT NOT NULL PRIMARY KEY UNIQUE, temp_hi INTEGER, temp_low INTEGER, data DATETIME)')