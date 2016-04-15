NHL API
=========

An (unofficial, read-only) API for nhl.com and other online resources related to the National Hockey League.

### Table of Contents
* [Background Information](#background-information)
* [API Usage](#api-usage)
* [Features](#features)
* [Installation](#installation)
* [Contributing](#contributing)

# Background Information

The NHL has an internal API that they don't release to the public. However, it's somewhat exposed, and this unofficial API leverages
this in order to create a cohesive solution with consistent endpoints. There's also a fair bit of data sanitization involved because
over the years the NHL has randomly made changes to their json formatting of various things, and sometimes their stuff just doesn't work.
Hopefully, this will allow developers to leverage the NHL's data without needing to do a bunch of trial and error. Big ups to 
[this guy from the hf boards](http://hfboards.hockeysfuture.com/showthread.php?t=1596119) for a bunch of network traffic analysis and 
endpoint discovery.

# API Usage
### API Base URL: `http://nhlapi.nickoman.me`

## Endpoints Summary
* GET: [`/games/<user>`](#get-usersuser)
  * GET: [`/users/<user>/activity`](#get-usersuseractivity)
    * GET: `/users/<user>/activity/answers`
    * GET: `/users/<user>/activity/user_follows`
    * GET: `/users/<user>/activity/want_answers`
    * GET: `/users/<user>/activity/upvotes`
    * GET: `/users/<user>/activity/review_requests`
* GET: [`/questions/<question>`](#get-questionsquestion)


### GET: `/games/<team>/<season>/<month>`

Gets the game_ids for the games in a team's given month of a given season. Pass 0 as the month to get
game_ids from the whole year.

#### Example
Example usage: `GET http://nhl.nickoman.me/games/MIN/2015/0`

Example result:
```json
{"games": ["2014010087", "2014010101", "2014020014", "2014020029", "2014020062", "2014020074", "2014020097", "2014020114", "2014020122",
 "2014020124", "2014020145", "2014020162", "2014020179", "2014020189", "2014020205", "2014020220", "2014020238", "2014020249", "2014020261",
 "2014020280", "2014020298", "2014020315", "2014020329", "2014020343", "2014020351", "2014020372", "2014020387", "2014020415", "2014020430",
 "2014020444", "2014020461", "2014020465", "2014020488", "2014020507", "2014020520", "2014020536", "2014020549", "2014020562", "2014020572",
 "2014020588", "2014020603", "2014020614", "2014020625", "2014020633", "2014020645", "2014020669", "2014020680", "2014020687", "2014020706",
 "2014020719", "2014020741", "2014020752", "2014020780", "2014020794", "2014020805", "2014020815", "2014020828", "2014020844", "2014020855",
 "2014020872", "2014020891", "2014020901", "2014020913", "2014020930", "2014020947", "2014020958", "2014020965", "2014020982", "2014020997",
 "2014021016", "2014021026", "2014021045", "2014021057", "2014021066", "2014021085", "2014021090", "2014021112", "2014021125", "2014021159",
 "2014021175", "2014021187", "2014021196", "2014021209", "2014021226", "2014030151", "2014030152", "2014030153", "2014030154", "2014030155",
 "2014030156", "2014030231", "2014030232", "2014030233", "2014030234", "2014010016", "2014010040", "2014010053", "2014010066"]}
```

### Get: `/events/<fullyear>/<game_id>`

Gets the ext_ids for events from a game_id during a given fullyear (e.g 20142015).

#### Example
Example usage: `GET http://nhl.nickoman.me/events/MIN/2015/0`

Example result:
```json
{"events": ["2014020280-466-h", "2014020280-466-a", "2014020280-59-h", "2014020280-59-a", "2014020280-712-h", "2014020280-712-a", "2014020280-99-h",
"2014020280-99-a", "2014020280-338-h", "2014020280-338-a", "2014020280-490-h", "2014020280-490-a", "2014020280-91-h", "2014020280-91-a",
"2014020280-311-h", "2014020280-311-a", "2014020280-453-h", "2014020280-453-a", "2014020280-54-h", "2014020280-54-a", "2014020280-473-h",
"2014020280-473-a", "2014020280-79-h", "2014020280-79-a", "2014020280-230-h", "2014020280-230-a", "2014020280-344-h", "2014020280-344-a",
"2014020280-58-h", "2014020280-58-a", "2014020280-705-h", "2014020280-705-a", "2014020280-96-h", "2014020280-96-a", "2014020280-337-h",
"2014020280-337-a", "2014020280-461-h", "2014020280-461-a", "2014020280-487-h", "2014020280-487-a", "2014020280-90-h", "2014020280-90-a",
"2014020280-240-h", "2014020280-240-a", "2014020280-405-h", "2014020280-405-a", "2014020280-5-h", "2014020280-5-a", "2014020280-469-h",
"2014020280-469-a", "2014020280-75-h", "2014020280-75-a", "2014020280-214-h", "2014020280-214-a", "2014020280-341-h", "2014020280-341-a",
"2014020280-56-h", "2014020280-56-a", "2014020280-498-h", "2014020280-498-a", "2014020280-94-h", "2014020280-94-a", "2014020280-331-h",
"2014020280-331-a", "2014020280-457-h", "2014020280-457-a", "2014020280-481-h", "2014020280-481-a", "2014020280-85-h", "2014020280-85-a","2014020280-236-h", "2014020280-236-a", "2014020280-349-h", "2014020280-349-a"]}
```

### GET: `/events/<ext_id>`

Gets the details of an event associated with the given ext_id.

#### Example
Example usage: `Get http://nhl.nickoman.me/events/2014020280-341-h`

Example result:
```json
[{"shareable": true, "trackName": "Darcy Kuemper Save on Brayden Schenn (15:31/2nd)", "publishPoint": "http://e1.cdnak.neulion.com/nhl/vod/2014/11/20/280/2_280_min_phi_1415_h_discrete_phi341_save_1_1600.mp4?eid=677090&pid=677629&gid=3000&pt=1", "formats": "0", "releaseDate": "2014-11-20T19:00:00.000", "image": "www/thumbs/2014/11/20/677629_es.jpg", "id": "2014020280-341-h", "runtime": "0:16", "duration": "16", "name": "Darcy Kuemper Save on Brayden Schenn (15:31/2nd)", "bigImage": "www/thumbs/2014/11/20/677629_eb.jpg", "description": "Home broadcast - Minnesota Wild at Philadelphia Flyers - November 20, 2014"}]
```







# Features
### Currently implemented
* Game Schedules (game_ids)
* Events         (event_ids)
* Video Highlight URLs

### Todo
* Player Images
* Team Statistics
* Player Statistics

# Installation
You will need [Python 2](https://www.python.org/download/). [pip](http://pip.readthedocs.org/en/latest/installing.html) is recommended for installing dependencies.

To run the API locally:
```bash
$ pip install -r requirements.txt
$ python app.py
```

# Contributing
Submit pull requests or issues whenever you'd like!