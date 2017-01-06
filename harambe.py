#! python3
# harambe.py - groupme bot to get weather, espn fantasy football scores,
# post random pictures, and troll friends

import json
import requests
import sys
import bs4
import pprint
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
from random import randint

HOST_NAME = '0.0.0.0'
PORT_NUMBER = int(os.environ.get('PORT', 9000))

baseUrl = 'https://api.groupme.com/v3'
accessToken = '' # your access Token
tokenUrl = '?token=' + accessToken

bot_id = '' # insert your bot id

# Send HTTP POST request to post to group.
def post_group(content, pic_url):
	postdo_post = '/bots/post'
	resUrl = baseUrl + postdo_post
	params = {'bot_id' : bot_id, 'text' : content, 'picture_url' : pic_url}
	res = requests.post(resUrl, params)
	res.raise_for_status()

def get_weather(city):
	# uses google geocoding api to find a latitude and longitude for the city supplied
	# uses the latitude and longitude in Dark Sky's weather api to get weather for the specific location
	GOOGLEAPIKEY = '' # your key for Google's geocoding API
	DARKSKYAPIKEY = '' # your key for Dark Sky's weather data API
	city = city.replace(' ', '+') # replaces the space if state is also given e.g. 'gainesville, fl'
	googlebaseURL = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (city, GOOGLEAPIKEY) # URL for googles geocoding api
	res = requests.get(googlebaseURL)
	res.raise_for_status()
	geocodeData = json.loads(res.text)
	geocode = geocodeData['results'][0]['geometry']['location']
	latitude = geocode['lat']
	longitude = geocode['lng']
	darkskybaseURL = 'https://api.darksky.net/forecast/%s/%s,%s' % (DARKSKYAPIKEY, latitude, longitude)
	res = requests.get(darkskybaseURL)
	res.raise_for_status()
	weatherData = json.loads(res.text)
	degree_sign= u'\N{DEGREE SIGN}' # degree unicode character
	post_group(weatherData['currently']['summary'] + ', ' + str(weatherData['currently']['apparentTemperature']) + degree_sign + 'F. ' + weatherData['hourly']['summary'] + '\n\n' + weatherData['daily']['summary'], None)

def all_league_scores():
	# Posts all league scores for your ESPN fantasy football league
	leagueId = '' # insert your ESPN leagueId
	seasonId = '' # insert season year
	scoreboardUrl = 'http://games.espn.com/ffl/scoreboard?leagueId=%s&seasonId=%s' % (leagueId, seasonId)
	res = requests.get(scoreboardUrl)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	tag = soup.find_all(class_=['score', 'name', 'owners'])
	message = tag[0].get_text()+': '+tag[2].get_text()+'\n'+tag[3].get_text()+': '+tag[5].get_text()+'\n\n'+tag[6].get_text()+': '+tag[8].get_text()+'\n'+tag[9].get_text()+': '+tag[11].get_text()+'\n\n'+tag[12].get_text()+': '+tag[14].get_text()+'\n'+tag[15].get_text()+': '+tag[17].get_text()+'\n\n'+tag[18].get_text()+': '+tag[20].get_text()+'\n'+tag[21].get_text()+': '+tag[23].get_text()+'\n\n'+tag[24].get_text()+': '+tag[26].get_text()+'\n'+tag[27].get_text()+': '+tag[29].get_text()+'\n\n'+tag[30].get_text()+': '+tag[32].get_text()+'\n'+tag[33].get_text()+': '+tag[35].get_text()
	post_group(message, None)

def get_matchup_score(user_id):
	# posts the matchup score from ESPN for the user who asks
	groupMembers = {}
	""" ^ dictionary with key equal to groupme userID (from API)
	and value equal to members name e.g {'000000':'Walter'} """
	leagueId = '' # insert your ESPN leagueId
	seasonId = '' # insert season year
	scoreboardUrl = 'http://games.espn.com/ffl/scoreboard?leagueId=%s&seasonId=%s' % (leagueId, seasonId)
	res = requests.get(scoreboardUrl)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, 'html.parser')
	scores_tag = soup.find_all(class_='score')
	names_tag = soup.find_all(class_='name')
	owners_tag = soup.find_all(class_='owners')
	score_content_line1 = None
	score_content_line2 = None
	for i in range(0, 12):
		if owners_tag[i].get_text().lower().split(' ')[0] == groupMembers[user_id].lower().split(' ')[0]:
			score_content_line1 = names_tag[i].get_text() + ': ' + scores_tag[i].get_text()
			if i in range(1, 12, 2):
				score_content_line2 = names_tag[i-1].get_text() + ': ' + scores_tag[i-1].get_text()
			else:
				score_content_line2 = names_tag[i+1].get_text() + ': ' + scores_tag[i+1].get_text()
			post_group(str(score_content_line1) + '\n' + str(score_content_line2), None)
		i += 1

def get_last_message():
	if 'rip harambe' in message_lower:
		rip_harambe_list = ['https://img.ifcdn.com/images/ccb85b3923314524e7203fe0e4284bad6e1b01e42eda8550b9b8b7988cf6de5b_1.jpg', 'https://i.redd.it/33d6a5it8eix.png', 'http://i1.kym-cdn.com/photos/images/original/001/155/744/c2f.jpg', 'https://static1.squarespace.com/static/570a0f1f4c2f85652de746c9/570a10085559863dc7612dc9/57c8eb429de4bb1598ee2b40/1472873504170/HARAMBE+2.0+(CLEAN).jpg?format=1500w', 'https://getonfleek.com/pub/media/catalog/product/d/i/dicks_out_for_harambe_crewneck.png', 'http://i2.kym-cdn.com/photos/images/original/001/155/662/8c5.jpg', 'https://pics.onsizzle.com/trending-stephen-hawking-renowned-physicist-makes-1st-facebook-post-since-3030807.png', 'https://img.ifcdn.com/images/159f2467d9d557ab49311de6462365a2bd21804ad6ea135ca56aaa8b06599280_1.jpg', 'http://i.imgur.com/y5WoTDN.jpg']
		rip_harambe_length = len(rip_harambe_list)-1
		i = randint(0, rip_harambe_length)
		post_group(None, rip_harambe_list[i])
	elif 'harambe' in message_lower and 'my fantasy' in message_lower:
		get_matchup_score(my_id)
	elif 'harambe' in message_lower and 'league scores' in message_lower:
		all_league_scores()
	elif 'harambe' in message_lower and 'resurrect' in message_lower:
		post_group(None, 'https://i.groupme.com/1200x799.jpeg.1c2ae1fd84214f9681cccfa65650bd42')
	elif my_id == '': # insert a friends user_id for the bot to troll every so often
		i = randint(1, 50)
		if i == 25:
			post_group("", None) # insert the message for the bot to post
	elif 'harambe' in message_lower and 'weather' in message_lower:
		message_lower_index = message_lower.index('in')
		target = message_lower[message_lower_index + 3:].strip('?')
		get_weather(target)
	elif 'harambe' in message_lower and my_id != '13439387':
		post_group(sender_name + ', come in my cage you neanderthal and see what happens.', None)

class RequestHandler(BaseHTTPRequestHandler):

	def do_POST(s):
		# Respond to a post request
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write(bytes("Response success", "utf8"))
		content = int(s.headers.get_all('Content-Length')[0])
		post_body_bytes = s.rfile.read(content)
		post_body = post_body_bytes.decode('ascii')
		recentdata = json.loads(post_body)
		global original_message, message_lower, sender_name_lower, my_id, sender_name
		original_message = recentdata['text']
		message_lower = original_message.lower()
		sender_name = recentdata['name']
		print(sender_name)
		print(original_message)
		sender_name_lower = sender_name.lower()
		my_id = str(recentdata['user_id'])
		print(my_id)
		get_last_message()

if __name__ == '__main__':
	server_class = HTTPServer
	handler_class = BaseHTTPRequestHandler
	server_address = (HOST_NAME, PORT_NUMBER)
	httpd = server_class(server_address, RequestHandler)
	print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
