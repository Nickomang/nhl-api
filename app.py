from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
	wild = {'Upcoming Season Champions': 'Minnesota Wild'}
	return json.dumps(wild)

####################################################################
# team_stats
####################################################################
@app.route('/<team>/roster')
def get_roster(team):
	url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/teamroster/" + str(team).upper() +"/iphone/clubroster.json"
	response = requests.get(url).json()
	return json.dumps(response)

####################################################################
# team_stats
####################################################################
@app.route('/<team>/stats/<season>/<form>')
def get_player_stats(team, season, form):
	url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/playerstatsline/" + season + "/" + form + "/" + team + "/iphone/playerstatsline.json"
	response = requests.get(url).json()
	return json.dumps(response)

####################################################################
# game_ids
####################################################################
# ISSUE with fullyear for 20152016
@app.route('/<team>/games/<int:season>/<int:month>', methods=["GET"])
def get_game_ids(team, season, month):
	game_ids = []

	# FULL YEAR
	if month == 0:
		for month in (10,11,12,1,2,3,4,5,6,7,8,9):
			if (month > 7):
				shortseason = str(season)[:-4]
			else:
				shortseason = str(season)[4:]
			url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + shortseason + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
			
			try:
				response = requests.get(url).json()
				for game in response['games']:
					if game['gameId']:
						game_ids.append(str(game['gameId']))
			except ValueError:
				print "nhl fucked up"

	# ANY MONTH 
	else:
		if (month > 7):
			season = str(season)[:-4]
		else:
			season = str(season)[4:]
		url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/clubschedule/" + team + "/" + season + "/" + str(month).zfill(2) + "/iphone/clubschedule.json"
		try:
			response = requests.get(url).json()
			for game in response['games']:
				if game['gameId']:
					game_ids.append(str(game['gameId']))
		except ValueError:
			print "nhl fucked up"
			
	json_game_ids = {"games": game_ids}
	return json.dumps(json_game_ids)

####################################################################
# ext_ids
####################################################################
@app.route('/events/<season>/<game_id>', methods=["GET"])
def get_ext_ids(game_id, season):
	url = "http://live.nhle.com/GameData/" + season + "/" + game_id + "/gc/gcgm.jsonp"
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
	json_ext_ids = {"events": ext_ids}
	return json.dumps(json_ext_ids)

####################################################################
# event descriptions
####################################################################
@app.route('/events/<ext_id>', methods=["GET"])
def get_event_description(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	return json.dumps(requests.get(url).json())


####################################################################
# highlight_urls
####################################################################
@app.route('/videos/<ext_id>', methods=["GET"])
def get_highlight_url(ext_id):
	url = "http://video.nhl.com/videocenter/servlets/playlist?ids=" + ext_id + "&format=json"
	response = requests.get(url).json()
	return response[0]['publishPoint']



####################################################################
# player images
####################################################################
@app.route('/images/<name>', methods=["GET"])
def get_player_image(name):
	url = "http://tsnimages.tsn.ca/ImageProvider/PlayerHeadshot?seoId=" + name
	return url


####################################################################
# Run app
####################################################################
if __name__ == '__main__':
    app.run(debug=True)