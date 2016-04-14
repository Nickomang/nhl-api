from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

# Gets a list of all game_ids for a give team/season/month
# 0 as the month returns the whole year
@app.route('/ids/<team>/<int:season>/<int:month>', methods=["GET"])
def get_game_ids(team, season, month):
	game_ids = []

	# FULL YEAR
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
				print "nhl fucked up"	
	# ANY MONTH 
	else:
		if (month > 7):
			url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season-1) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
		else:
			url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + str(season) + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
		
		try:
			response = requests.get(url).json()
			for game in response['games']:
				if game['gameId']:
					game_ids.append(str(game['gameId']))
		except ValueError:
			print "nhl fucked up"

	json_game_ids = {"games": game_ids}
	return json.dumps(json_game_ids)

# Returns a list of ext_ids for a given game_id
@app.route('/events/<fullyear>/<game_id>')
def get_ext_ids(game_id, fullyear):
	url = "http://live.nhle.com/GameData/" + fullyear + "/" + game_id + "/gc/gcgm.jsonp"
	if (not requests.get(url)):
		print "NHL fucked up"
		return json.dumps([])
	response = requests.get(url).text

	# Necesarry because sometimes the NHL has game ids that don't actually correspond to anything
	print "using game", game_id
	trimmed_response = response[10:-1]
	try:
		json_response = json.loads(trimmed_response)
	except ValueError:
		print "NHL fucked up again"
		trimmed_response = response[10:-2]
		try:
			json_response = json.loads(trimmed_response)
		except ValueError:
			print "THEY FUCKED UP A THIRD TIME"
			trimmed_response = response[10:-3]
			try:
				json_response = json.loads(trimmed_response)
			except ValueError:
				print "Fuck bettman"
				return json.dumps([])
	
	# # This block is because sometimes the NHL fucks up and the older ones need the newer treatment
	# try:
	# 	json_response = json.loads(trimmed_response)
		
	# except ValueError:
	# 	trimmed_response = response[10:-1]
	
	json_response = json.loads(trimmed_response)
	ext_ids = []

	# Needs this because the NHL inexplicably sometimes uses events and sometimes uses ingame
	key = ''
	if(json_response['video']['events']):
		key = 'events'
	elif(json_response['video']['ingame']):
		key = 'ingame'
	else:
		return ext_ids

	for event in json_response['video'][key]:
		if 'type' in event:
			for feed in event['feeds']:
				ext_ids.append(str(feed['extId']))
	return json.dumps(ext_ids)


if __name__ == '__main__':
    app.run(debug=True)