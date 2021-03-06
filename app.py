from flask import Flask, jsonify, make_response
import requests
import re
import json
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def index():
	wild = {'Upcoming Season Champions': 'Minnesota Wild'}
	return json.dumps(wild)

# New stuff
# nhl.com/gamecenter/<game_id>
# new_game_id = <game_id> - first four (year)
# GS = game summary

# http://media.sny.tv/sny/2015/10/06/sny_519968983_1m.mp4
# 23.200.219.120
# http://md-akc.med.nhl.com/mp4/nhl/2016/04/25/822f98ff-8065-454b-8d85-cd692db8daa4/1461548688943/asset_1800k.mp4

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
	try:
		url = "http://nhlwc.cdnak.neulion.com/fs1/nhl/league/playerstatsline/" + season + "/" + form + "/" + team + "/iphone/playerstatsline.json"
		response = requests.get(url).json()
		pattern = re.compile("^\s+|\s*,\s*|\s+$")
		for skater in response['skaterData']:
			line = skater['data']
			data = [x for x in pattern.split(line) if x]
			skater['data'] = {
				"Number": data[0],
				"Position": data[1],
				"PlayerName": data[2],
				"GamesPlayed": data[3],
				"Goals": data[4],
				"Assists": data[5],
				"Points": data[6],
				"PlusMinus": data[7],
				"PenaltyMinutes": data[8],
				"Shots": data[9],
				"TimeOnIce": data[10],
				"PowerPlayPoints": data[11],
				"ShorthandedPoints": data[12],
				"GameWinningGoals": data[13],
				"OvertimeGoals": data[14]
			}
			# #, POS, NAME, GP, G, A, P, +/-, PIM, S, TOI/G, PP, SH, GWG, OT
		for goalie in response['goalieData']:
			line = goalie['data']
			data = [x for x in pattern.split(line) if x]
			goalie['data'] = {
				"Number": data[0],
				"Position": data[1],
				"PlayerName": data[2],
				"GamesPlayed": data[3],
				"Wins": data[4],
				"Losses": data[5],
				"OvertimeLosses": data[6],
				"GoalsAgainst": data[7],
				"ShotsAgainst": data[8],
				"Saves": data[9],
				"SavePCT": data[10],
				"GoalsAgainstAverage": data[11],
				"Shutouts": data[12],
				"PenaltyMinutes": data[13],
				"Minutes": data[14]
			}
			# POS, NAME, GP, W, L, OT, GA, SA, Sv, SV%, GAA, SO, PIM, Min
	except ValueError:
		return json.dumps({})
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
				print "NHL fucked up their data"

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
			print "NHL fucked up their data"
			
	json_game_ids = {"games": game_ids}
	return json.dumps(json_game_ids)


####################################################################
# ext_ids
####################################################################
@app.route('/events/<season>/<game_id>', methods=["GET"])
def get_ext_ids(game_id, season):
	url = "http://live.nhle.com/GameData/" + season + "/" + game_id + "/gc/gcgm.jsonp"
	if (not requests.get(url)):
		print "NHL fucked up their data"
		return json.dumps([])
	response = requests.get(url).text

	# Necesarry because sometimes the NHL has game ids that don't actually correspond to anything
	print "using game", game_id
	trimmed_response = response[10:-1]
	try:
		json_response = json.loads(trimmed_response)
	except ValueError:
		print "NHL fucked up their data even worse"
		trimmed_response = response[10:-2]
		try:
			json_response = json.loads(trimmed_response)
		except ValueError:
			print "WOW, THEY FUCKED UP A THIRD TIME"
			trimmed_response = response[10:-3]
			try:
				json_response = json.loads(trimmed_response)
			except ValueError:
				print "Empty event, good one Bettman"
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
	response = requests.get(url).text
	trimmed_response = response[9:-1] # Should be 9:-1, but if problems arise do it using REGEX
	json_response = json.loads(trimmed_response)
	return json.dumps(json_response)


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
# team svgs
####################################################################
@app.route('/<team>/logo', methods=["GET"])
def get_team_logo(team):
	paths = {
		'BOS': 6,
		'BUF': 7,
		'DET': 17,
		'FLO': 13,
		'MTL': 8,
		'OTT': 9,
		'TBL': 14,
		'TOR': 10,
		'CAR': 12,
		'CBJ': 29,
		'NJD': 1,
		'NYI': 2,
		'NYR': 3,
		'PHI': 4,
		'PIT': 5,
		'WSH': 15,
		'CHI': 16,
		'COL': 21,
		'DAL': 25,
		'MIN': 30,
		'NSH': 18,
		'STL': 19,
		'WPG': 52,
		'ANA': 24,
		'ARI': 53,
		'CGY': 20,
		'EDM': 22,
		'LAK': 26,
		'SJS': 28,
		'VAN': 23
	}
	path = paths[team]
	url = "http://www-league.nhlstatic.com/builds/site-core/a46bb6bad4f43e92f7fc3d3ddfc2c0b26a717cae_1461274874/images/team/logo/current/" + str(path) + "_dark.svg"
	response = requests.get(url)
	return response.content


####################################################################
# team stats/standings
####################################################################
@app.route('/<team>/stats', methods=["GET"])
def get_team_stats(team):
	
	url = "http://app.cgy.nhl.yinzcam.com/V2/Stats/Standings"

	try:
		response = requests.get(url)
		root = ET.fromstring(response.content)
	except ET.ParseError:
		print "xml structure changed or bad url specified"
		return json.dumps({})

	try:
		standingNode = root.find("Conference/StatsSection/Standing[@TriCode='" + team + "']")
		statsGroup1 = standingNode.find("StatsGroup[@Order='1']")
		statsGroup2 = standingNode.find("StatsGroup[@Order='2']")
	except AttributeError:
		print ("xml structure screwed up/nonexistant team specified")
		return json.dumps({})
		
	return json.dumps({
		"LeagueRank": standingNode.get("LeagueRank"),
		"ConferenceRank": standingNode.get("ConfRank"),
		"DivisionRank": standingNode.get("DivRank"),
		"GamesPlayed": statsGroup1.get("Stat0"),
		"Wins": statsGroup1.get("Stat1"),
		"Losses": statsGroup1.get("Stat2"),
		"OvertimeLosses": statsGroup1.get("Stat3"),
		"Points": statsGroup1.get("Stat4"),
		"GoalsFor": statsGroup2.get("Stat0"),
		"GoalsAgainst": statsGroup2.get("Stat1"),
		"LastTen": statsGroup2.get("Stat2"),
		"Streak": statsGroup2.get("Stat3")
	})	

	
####################################################################
# Run app
####################################################################
if __name__ == '__main__':
    app.run(debug=True)