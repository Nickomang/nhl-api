from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

# Gets a list of all game_ids for a give team/season/month
# 0 as the month returns the whole year
@app.route('/ids/<team>/<int:season>/<int:month>')
def get_game_ids(team, season, month):
	game_ids = []

	if month == 0:
		for month in (10,11,12,1,2,3,4,5,6,7,8,9):
			if (month > 7):
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season-1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			else:
				url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			try:
				response = requests.get(url).json()
				for game in response['games']:
					game_ids.append(str(game['gameId']))
			except ValueError:
				game_ids.append('')		
	else:
		if (month > 7):
			url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season-1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
		else:
			url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
		response = requests.get(url).json()
		for game in response['games']:
			game_ids.append(str(game['gameId']))
	return json.dumps(game_ids)

if __name__ == '__main__':
    app.run(debug=True)