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
| GET	        | /ids/{team}/{season>}/{month} | Returns a json object with game_ids from the given month. Pass 0 as month to get the whole year.
| GET			| /events/{fullyear}/{month}    | Returns a json object with ext_ids from the game_id.