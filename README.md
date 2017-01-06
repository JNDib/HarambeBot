# HarambeBot
GroupMe Bot to get weather, ESPN fantasy football scores, and troll friends. Yes, this is a tribute to the GOAT, Harambe.

## Features
This bot is able to post weather data from any city in the world, scrape ESPN's standings fantasy football page for a specific league and return scores, as well as randomly troll friends. 

### Requirements for Usage
- Google account to use Google's geocoding API
- Dark Sky API account to access weather data using the coordinates returned for a given city from Google's geocoding API
- ESPN fantasy football league to get scores
- GroupMe account, of course

## Usage
To use this bot, you will need to establish a server. To host my bot, I used Heroku, however there are many different web hosting services available. When a message is posted in the GroupMe chat your bot resides in, GroupMe pings the callback url for your bot with a POST request. The text content of this request is then received, decoded to ASCII characters, and formatted using JSON. 
