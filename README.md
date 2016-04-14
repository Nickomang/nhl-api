Quora API
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
### API Base URL: `http://nhl.nickoman.me`

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

Gets the game_ids for the games in a team's given month of a given season. You can pass 0 as the month to get
game_ids from the whole year

#### Example
Example usage: `GET http://nhl.nickoman.me/games/MIN/2015/0`

Example result:
```json
{"games": ["2014010087", "2014010101", "2014020014", "2014020029", "2014020062", "2014020074", "2014020097", "2014020114", "2014020122",
 "2014020124", "2014020145", "2014020162", "2014020179", "2014020189", "2014020205", "2014020220", "2014020238", "2014020249", "2014020261",
  "2014020280", "2014020298", "2014020315", "2014020329", "2014020343", "2014020351", "2014020372", "2014020387", "2014020415", "2014020430",
   "2014020444", "2014020461", "2014020465", "2014020488", "2014020507", "2014020520", "2014020536", "2014020549", "2014020562", "2014020572",
    "2014020588", "2014020603", "2014020614", "2014020625", "2014020633", "2014020645", "2014020669", "2014020680", "2014020687", "2014020706", "2014020719", "2014020741", "2014020752", "2014020780", "2014020794", "2014020805", "2014020815", "2014020828", "2014020844", "2014020855",
     "2014020872", "2014020891", "2014020901", "2014020913", "2014020930", "2014020947", "2014020958", "2014020965", "2014020982", "2014020997",
      "2014021016", "2014021026", "2014021045", "2014021057", "2014021066", "2014021085", "2014021090", "2014021112", "2014021125", "2014021159",
       "2014021175", "2014021187", "2014021196", "2014021209", "2014021226", "2014030151", "2014030152", "2014030153", "2014030154", "2014030155", "2014030156", "2014030231", "2014030232", "2014030233", "2014030234", "2014010016", "2014010040", "2014010053", "2014010066"]}
```


### GET: `/users/<user>`
#### Example
Example usage: `GET http://quora.christopher.su/users/Christopher-J-Su`

Example result:
```json
{
  "answers": 301, 
  "blogs": null, 
  "edits": 5576, 
  "followers": 173, 
  "following": 167, 
  "name": "Christopher-J-Su", 
  "posts": 6, 
  "questions": 110, 
  "topics": null, 
  "username": "Christopher-J-Su"
}
```
Note: due to recent Quora UI changes, the `blogs` and `topics` statistics are currently not working and will always return `null`.

### GET: `/users/<user>/activity`
Get the user's activity.
#### Example
Example usage: `GET http://quora.christopher.su/users/Christopher-J-Su/activity`

Output (excerpt):
```json
{
  "activity": [
    {
      "link": "http://www.quora.com/University-of-Washington/What-does-the-UW-CS-department-gain-from-barring-other-UW-students-from-taking-its-courses/answer/Christopher-J-Su", 
      "published": "Tue, 25 Feb 2014 00:10:55 GMT", 
      "summary": "<-- ... --->", 
      "title": "What does the UW CS department gain from barring other UW students from taking its courses?"
    }, 
    {
      "link": "http://www.quora.com/Can-applied-math-students-take-CSE-majors-only-courses/answer/Christopher-J-Su", 
      "published": "Tue, 25 Feb 2014 00:04:33 GMT", 
      "summary": "<div style=\"color: #666666;\">Christopher J. Su added this answer.</div><br /><div id=\"ld_ihbjvp_3370\"><div style=\"font-weight: bold; color: #000000;\"><div class=\"hover_menu hidden hover_menu_wide hover_menu_cards\" id=\"__w2_qIjTQfx_menu\" style=\"display: none;\"><div class=\"hover_menu_nub\"></div><div class=\"hover_menu_contents\" id=\"__w2_qIjTQfx_menu_contents\"> </div></div><a class=\"user\" href=\"http://www.quora.com/Christopher-J-Su\" id=\"__w2_qIjTQfx_link\">Christopher J. Su</a></div><br />I think you might need to fill out a CSE course petition to take a 300+-level CSE course as a non-major: <span class=\"qlink_container\"><a class=\"external_link\" href=\"https://www.cs.washington.edu/prospective_students/undergrad/petition/\" target=\"_blank\">Petition for Non-Majors</a></span>.<br /><br /><a href=\"http://www.quora.com/Can-applied-math-students-take-CSE-majors-only-courses\" style=\"font-weight: bold;\">See question on Quora</a></div>", 
      "title": "Can applied math students take CSE majors only courses?"
    }
  ], 
  "last_updated": "Thu, 24 Jul 2014 05:32:49 GMT", 
  "username": "Christopher-J-Su"
}
```

### GET: `/users/<user>/activity/answers`
Get the user's latest answers.
#### Example
Example usage: `GET http://quora.christopher.su/users/Christopher-J-Su/activity/answers`

Output (excerpt):
```json
{
  "items": [
    {
      "id": "5:48afe1749959ac2b673b1094a13b6cb5#1418975956225507", 
      "link": "http://www.quora.com/I-need-a-summer-internship-but-I-dont-want-to-apply-because-theres-a-90-chance-Ill-get-rejected-What-should-I-do/answer/Christopher-J-Su", 
      "published": "Fri, 19 Dec 2014 07:59:16 GMT", 
      "summary": "<div id=\"ld_ftujiv_1299\"><div style=\"font-weight: bold; color: #000000;\"><div class=\"hover_menu hidden hover_menu_cards hover_menu_wide hover_menu_cards\" id=\"__w2_lHemksQ_menu\" style=\"display: none;\"><div class=\"hover_menu_nub\"></div><div class=\"hover_menu_contents\" id=\"__w2_lHemksQ_menu_contents\"> </div></div><a class=\"user\" href=\"http://www.quora.com/Christopher-J-Su\" id=\"__w2_lHemksQ_link\">Christopher J. Su</a></div><br />Apply, interview, fail, repeat. Keep failing. Eventually, you&#039;ll notice you stop failing as much as you did before. Then, you&#039;ll suddenly start passing interviews. Then, you&#039;ll start getting offers.<br /><br />Don&#039;t get locked up in the mindset that you won&#039;t make it. If you never even try, you&#039;ll never get an internship. Having interviews scheduled will motivate you to study and prepare for them. Doing the interviews themselves is great practice.<br /><br /><a href=\"http://www.quora.com/I-need-a-summer-internship-but-I-dont-want-to-apply-because-theres-a-90-chance-Ill-get-rejected-What-should-I-do\" style=\"font-weight: bold;\">See question on Quora</a></div>", 
      "title": "I need a summer internship, but I don't want to apply because there's a 90% chance I'll get rejected. What should I do?"
    }
  ]
}
```

# Features
### Currently implemented
* User statistics
* User activity
* Question statistics
* Answer statistics

### Todo
* Detailed user information (followers, following, etc.; not just statistics)
* Unit tests
* Cache data with memcached

# Installation
You will need [Python 2](https://www.python.org/download/). [pip](http://pip.readthedocs.org/en/latest/installing.html) is recommended for installing dependencies.

To run the API locally:
```bash
$ pip install -r requirements.txt
$ python app.py
```

# Contributing
Submit pull requests or issues whenever you'd like!