# FINAL PROJECT - SI 206
# JOHN FALCONE
import requests
import json
import facebook
import pprint
import sqlite3
from datetime import date, datetime

try:
	import api_codes
	facebook_token = api_codes.facebook_token
	api_key = api_codes.weather_token
	news_token = api_codes.news_token
except:
	pass


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

#######################
#########WEATHER#######
#######################
#api_key = api_codes.weather_token

print("Fetching most recent date of Facebook Like")
like_date = date_data[0]
unix_time = time_data[0]
#print (type(like_date))
#print (type(unix_time))
#print(like_date)
#print(unix_time)
#like_date = "2017-12-12"
#unix_time = "2017-12-12T00:13:42+0000"

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
if like_date == stored_date:
	print("Like Date matches Storage Date. Cached data is up-to-date.")

#condition - if unix-date from cache DOES NOT EQUAL unix date from facebook call, do this. That means that dates have changed
#tups_for_print = []
try:
	if stored_date != like_date:
		print("Stored data is not the most recent. Fetching weather data. This may take some time!")
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
			#weather_tup2 = "City: "city_name, "High: " high_temp, "Low": low_temp
			#tups_for_print.append(weather_tup2)
			cur.execute('INSERT INTO WEATHER (city, temp_hi, temp_low, data) VALUES (?,?,?,?)',weather_tup)

	else:
		print("Weather Data in SQL Database is up to date. No need to make request to DarkSky API!")

except:
	print("Unable to reach DarkSky API. Referring to cached data.")


conn.commit()
#conn.close()


#cur.execute('INSERT INTO WEATHER (city, temp_hi, temp_lo, data) VALUES (?,?,?,?)',tup1)
############################
####### NEWS ###############
############################
#news_token = api_codes.news_token

#url = ("https://newsapi.org/v2/top-headlines?sources=the-new-york-times&apiKey=" + news_token)
try:
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

	if stored_date != like_date:

		file=open("news_source.txt", "w")

		for item in data_tups[:5]:
			file.write(item[0] + "\n")
			file.write(item[1] + "\n")
			file.write("***" + "\n")

		file.close()


	else:
		print("Headline Data in cache file is up to date. No need to make request to News API!")
except:
	print("Unable to reach News API. Referring to cached data.")


###########################
######## OUTPUT ###########
###########################

print("\n")
print("*** DATA SUMMARY ***")
print("Welcome to the data summary! Here, you can see the data that the program has collected. Let's go one API at a time. First, using a call to the Facebook API, we received the date of your most recent post like.")
print("\n")
print("Your most recent post like occured on: " + like_date)
print("\n")
print("Using that date, the DarkSky API can be called. The DarkSky API can take a timestamp as input and return historical weather data. Take a look at what the high and low temperatures were on that date in all 50 US state captials.")
print("\n")
print("On " + like_date + " the high and low temperatures in US state capitols were:")
weather_output = []
for row in cur.execute('SELECT * FROM WEATHER'):
	weather_output.append(row)
	#print(row)
weather_output_2 = sorted(weather_output)
for x in weather_output_2:
	#print("City: " + x[0] + " High: " + str(x[1]) + " Low: " + str(x[2]))
	print("{: <15} High: {: <5} Low: {: <5}".format(*x))
print("\n")
print("Pretty cool, right? Now, let's use the News API to dig up the top news stories from that day. Summaries of the five most popular articles from CNN can be found below.")
print("*********************")
print("\n")
file=open("news_source.txt", "r")
for line in file:
	print(line)
print("\n")
print("There you go. Those are some great examples of the power of APIs. Thanks for using my program! - John")

file.close()
conn.close()