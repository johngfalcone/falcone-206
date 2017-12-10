# FINAL PROJECT - SI 206
# JOHN FALCONE
import requests
import json
import facebook
import api_codes
import pprint
import sqlite3
from datetime import date, datetime

facebook_token = api_codes.facebook_token


#open/create the cache file!
CACHE_FNAME = "facebook_data_cache.json"
# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

def get_facebook_data(me):

	if me in CACHE_DICTION:
		print("Data in the cache")
		results = CACHE_DICTION[me]
		return results

	else:
		print("Fetching")
		graph = facebook.GraphAPI(facebook_token)
		results = graph.get_object("me", fields = "id,name,likes", limit=100)
		CACHE_DICTION[me] = results

		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return results

facebook_data = get_facebook_data("me")
likes_data = []
time_data = []
date_data = []
time_data_fixed = []

for x in facebook_data["likes"]["data"]:
	likes_data.append(x)
	timestamp = x["created_time"]
	time_data.append(timestamp)

for x in time_data:
	y = x.split("T")
	date_data.append(y[0])

for x in time_data:
	x = x.replace("T", " ")
	time_data_fixed.append(x)


############################
####### NEWS ###############
############################
news_token = api_codes.news_token

like_date = date_data[0]
unix_time = time_data[0]
#url = ("https://newsapi.org/v2/top-headlines?sources=the-new-york-times&apiKey=" + news_token)
url2 = ("https://newsapi.org/v2/everything?sources=cnn&from={}&to={}&sortBy=popularity&apiKey=" + news_token).format(like_date,like_date)
#url3 = ("https://newsapi.org/v2/everything?sources=cnn&from=2016-12-15&to=2016-12-20&sortBy=popularity&apiKey=" + news_token)
#print(url2)
response = requests.get(url2)
news_data = json.loads(response.text)
#pprint.pprint(news_data)

titles_list = []
descriptions_list = []
for x in news_data["articles"]:
	titles_list.append(x["title"])
	descriptions_list.append(x["description"])
data_tups = list(zip(titles_list, descriptions_list))
#print(data_tups)

#######################
#########WEATHER#######
#######################
api_key = api_codes.weather_token

#US STATES
state_list = []
with open('state_data.json') as state_data:
    e = json.load(state_data)
for x in e.items():
	state_list.append((x[1]["name"], x[1]["capital"], x[1]["lat"], x[1]["long"]))


conn = sqlite3.connect("state_weather_db.sqlite")
cur = conn.cursor()
stored_dates = cur.execute("SELECT data FROM WEATHER")
stored_date = stored_dates.fetchone()[0]
#print(stored_date)
#print(like_date)

#condition - if unix-date from cache DOES NOT EQUAL unix date from facebook call, do this. That means that dates have changed
if stored_date != like_date:
	print("not equal")
	cur.execute('DELETE FROM WEATHER')

	for item in state_list:

		city_name = item[1]
		lat = item[2]
		lng = item[3]


		request_url = "https://api.darksky.net/forecast/{}/{},{},{}".format(api_key, lat, lng, unix_time)
		#print(request_url)
		darksky_response = requests.get(request_url)
		darksky_data = json.loads(darksky_response.text)
		#pprint.pprint(darksky_data)

		high_temp = int(darksky_data["daily"]["data"][0]["temperatureHigh"])
		low_temp = int(darksky_data["daily"]["data"][0]["temperatureLow"])
		#print(high_temp)
		#print(low_temp)
		#capital_temps.append((city_name, high_temp, low_temp, unix_time))
		weather_tup = city_name, high_temp, low_temp, like_date
		cur.execute('INSERT INTO WEATHER (city, temp_hi, temp_low, data) VALUES (?,?,?,?)',weather_tup)

else:
	print("Weather Data in SQL Database is up to date. No need to make request to DarkSky API!")


conn.commit()
conn.close()


#cur.execute('INSERT INTO WEATHER (city, temp_hi, temp_lo, data) VALUES (?,?,?,?)',tup1)
