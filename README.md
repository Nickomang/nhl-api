# NHL Api



## Endpoints

/api before each of these

Game_ids
day (for all teams)
/ids/{date} (yyyy-mm-dd)

month (pass 0 for year) (for a team)
/ids/{team}/{year}/{month}


Events (ext_id's)
/events/season/{game_id}

Video highlight
/highlights/{ext_id}

Player image
/image/{name} (hyphens instead of spaces, replace apostraphe and dot with nothing)




## Api endpoints
| Method        | Endpoint           				| Usage  		|
| ------------- |:-------------:				| -------------:|
| GET	        | /events/{season>}/{game_id}          | Returns a json object with all events from the game
| GET	        | /highlights/{ext_id}         | Returns a json object with all events from the game