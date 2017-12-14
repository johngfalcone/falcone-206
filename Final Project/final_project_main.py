# FINAL PROJECT - SI 206
# JOHN FALCONE
import requests
import json
import facebook
import pprint
import sqlite3
from datetime import date, datetime

#Here, the program calls for the api_codes file and the necessary api files. If the file doesn't exist, the code moves on, indicating that all of the data used will be from their respective cache files.
try:
	import api_codes
	facebook_token = api_codes.facebook_token
	api_key = api_codes.weather_token
	news_token = api_codes.news_token
except:
	pass


#Here, the cache file for the faecbook data is read.
CACHE_FNAME = "facebook_data_cache.json"
try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

#This function calls to the Facebook API if the data is out of date. It uses the "me" object as its only parameter.
def get_facebook_data(me):

	if me in CACHE_DICTION:
		print("Data in the cache")
		results = CACHE_DICTION[me]
		return results

	else:
		print("Fetching")
		#Facebook's graph API is called, after which the results are returned. The results contain a list of the most recent likes a user has made, including the unix time the interaction occured.
		graph = facebook.GraphAPI(facebook_token)
		results = graph.get_object("me", fields = "id,name,likes", limit=100)
		CACHE_DICTION[me] = results

		#The newly-called data is stored in the cached, and now considered the most up-to-date data.
		f = open(CACHE_FNAME, "w")
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	return results

#The following set of for loops extract the data from the Facebook call.
facebook_data = get_facebook_data("me")
likes_data = []
time_data = []
date_data = []
time_data_fixed = []

#Here, a list of the likes (and their data) is extracted.
for x in facebook_data["likes"]["data"]:
	likes_data.append(x)
	timestamp = x["created_time"]
	time_data.append(timestamp)

#This function seperates all of the unix timestamps into readable datestamps.
for x in time_data:
	y = x.split("T")
	date_data.append(y[0])

#I don't think this loop actually does anything consequential.
for x in time_data:
	x = x.replace("T", " ")
	time_data_fixed.append(x)

#########################
######## WEATHER ########
#########################

#Because the previous loops created lists of Facebook like data, index[0] of that data provides the most recent set.
print("Fetching most recent date of Facebook Like.")
like_date = date_data[0]
unix_time = time_data[0]

#Open the json file containing data on state capitols. Each object contains the state name, capitol name, capitol latitude, and capitol longitude.
#This data is moved from json into a list of tuples, containing all of the relevant data.
state_list = []
with open('state_data.json') as state_data:
    e = json.load(state_data)
for x in e.items():
	state_list.append((x[1]["name"], x[1]["capital"], x[1]["lat"], x[1]["long"]))

#The SQLite database connection is opened. The stored date is fetched from the file. The stored date contains the date of the last time the data in the file was changed.
conn = sqlite3.connect("state_weather_db.sqlite")
cur = conn.cursor()
stored_dates = cur.execute("SELECT data FROM WEATHER")
stored_date = stored_dates.fetchone()[0]

#The stored date is compared against the like date. If they're equal, the cached data is up to date. If not, the API needs to be called, and new data must be fetched.
if like_date == stored_date:
	print("Like Date matches Storage Date. Cached data is up-to-date.")

#This block is in a try because if the API doesn't go through (API down, api codes don't exist, etc.) the code can continue on using the cached data.
try:
	if stored_date != like_date:
		print("Stored data is not the most recent. Fetching weather data. This may take some time!")
		cur.execute('DELETE FROM WEATHER')

		#This loop iterates through each state in the list of states, extracting the city name, capitol, and longitude for use in the DarkSky API call.
		for item in state_list:
			city_name = item[1]
			lat = item[2]
			lng = item[3]

			#The DarkSky API is called using the state data. The unix_time parameter is taken from the Facebook data.
			request_url = "https://api.darksky.net/forecast/{}/{},{},{}".format(api_key, lat, lng, unix_time)
			darksky_response = requests.get(request_url)
			darksky_data = json.loads(darksky_response.text)

			#From the returned data, the daily high and low temperatures are stored in varibles
			high_temp = int(darksky_data["daily"]["data"][0]["temperatureHigh"])
			low_temp = int(darksky_data["daily"]["data"][0]["temperatureLow"])

			#All of the data collected is put into a new tuple, which is then stored in the SQL cache. This is done for all 50 states.
			weather_tup = city_name, high_temp, low_temp, like_date
			cur.execute('INSERT INTO WEATHER (city, temp_hi, temp_low, data) VALUES (?,?,?,?)',weather_tup)

	else:
		print("Weather Data in SQL Database is up to date. No need to make request to DarkSky API!")

except:
	print("Unable to reach DarkSky API. Referring to cached data.")

conn.commit()

#########################
#########  NEWS  ########
#########################

#Like the call to the DarkSky API, this block is in a try. In case something goes wrong with the API call, the program continues with cached data.
try:
	#The News API is called using the like date. This fetches the most popular CNN news articles from the date of your last Facebook like.
	url2 = ("https://newsapi.org/v2/everything?sources=cnn&from={}&to={}&sortBy=popularity&apiKey=" + news_token).format(like_date,like_date)
	response = requests.get(url2)
	news_data = json.loads(response.text)

	#From the returned data, lists of the article titles and article descriptions are created. They are then merged together, matching headlines with descriptions in a list of tuples.
	titles_list = []
	descriptions_list = []
	for x in news_data["articles"]:
		titles_list.append(x["title"])
		descriptions_list.append(x["description"])
	data_tups = list(zip(titles_list, descriptions_list))

	#This checks if the like date has changed. If it has, the data grabbed is stored in the cache and saved as the most recent data. This uses the same storage date as the weather data so that the two APIs are synchronous.
	if stored_date != like_date:

		#The headline and description from the five most popular articles are stored in a cache file. In this case, the cache is a .txt.
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

#The following outputs the data collected by the program in a readable way.
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
weather_output_2 = sorted(weather_output)
for x in weather_output_2:
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