# Capstone Final Project

Uploading the final project for the Full Stack Nanodegree Program at Udacity.

## User Roles:
### Casting Assistant

		Can view actors and movies

###Casting Director

		All permissions a Casting Assistant has and…
		Add or delete an actor from the database
		Modify actors or movies

###Executive Producer

		All permissions a Casting Director has and…
		Add or delete a movie from the database

## Instructions to set up authentication:

The app has no frontend for authentication, so you need to get the JWT Token by clicking the link below.
https://holecska.eu.auth0.com/authorize?audience=capstone_identifier&response_type=token&client_id=qhDJV70svVcNnjRkHUUtxqODyFqz1lTJ&redirect_uri=https://localhost:8080/login

### Logins:
	1. Casting Assistant
		Username: assistant@udacity.com
		Password: udacity@assistant2021
	2. Casting Director
		Username: director@udacity.com
		Password: udacity@director2021
	3. Executive Producer
		Username: producer@udacity.com
		Password: udacity@producer2021

## To run the unittest

ENV variables must be set to run the unittest python file.

token_assistant = {your access token for Casting Assistant}
token_director = {your access token for Casting Director}
token_producer = {your access token for Executive Producer}

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## API References

### Getting Started

#### The Application is hosted at:

https://udacity-capstone-adam-holecska.herokuapp.com/

- Authentication: This application requires an authentication, accessing tokens with above detailed usernames and passwords.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400/401: Authorization Errors
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable / Integrity Error / Attribute Error

### Endpoints

#### GET /movies
- General:
	Returns of an object with movies and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/movies`
- Returns
```
{
  "movies": [
				    {
							"id": 1,
							"title": "Joker",
							"release_date": "2019.10.25"
						},
						{
							"id": 1,
							"title": "Joker New",
							"release_date": "2020.10.25"
						}
  ],
  "success": true
}
```

#### GET /actors
- General:
	Returns of an object with actors and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/actors`
- Returns

```
    {
      "actors": [
    	    {
    				"age": 46,
    				"id": 1,
    				"name": "Actor 1",
    				"gender": "men"
    			},
    			{
    				"age": 26,
    				"id": 1,
    				"name": "Actor 1",
    				"gender": "women"
    			}
      ],
      "success": true
    }
```

#### POST /movies
- General:
	Add a new movie to the database and returns the currently added movie and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" "Authorization: Bearer {your token}"
    -d '{
    "title": "Joker",
    "release_date": "2019.10.03"}'`

- Returns:
```
{
    "movie": {
        "id": 11,
        "release_date": "Thu, 03 Oct 2019 00:00:00 GMT",
        "title": "Joker"
    },
    "success": true
}
```

#### POST /actors
- General:
	Add a new actor to the database and returns the currently added actor and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" "Authorization: Bearer {your token}"
    -d '{
    "name": "Joaquin Phoenix",
    "age": "46",
    "gender": "men"}'`

- Returns:
```
{
    "actor": {
		    "name": "Joaquin Phoenix",
		    "age": "46",
		    "gender": "men"
		},
    "success": true
}
```

#### PATCH /movies
- General:
	Change movie in the database and returns the currently modified movie and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/movies/<movie_id>/ -X PATCH -H "Content-Type: application/json" "Authorization: Bearer {your token}"
    -d '{
    "title": "Joker Modified"'`

- Returns:
```
{
    "changed_movie": <movie_id>,
    "success": true
}
```

#### PATCH /actors
- General:
	Change actor in the database and returns the currently modified actors's ID and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/actors/<actor_id>/ -X PATCH -H "Content-Type: application/json" "Authorization: Bearer {your token}"
    -d '{
    "age": 55}'`

- Returns:
```
{
    "changed_actor": <actor_id>,
    "success": true
}
```

#### DELETE /movies
- General:
	Remove a movie from the database and returns the currently deleted movie's ID and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/movies/<movie_id>/ -X DELETE -H "Content-Type: application/json" "Authorization: Bearer {your token}"`

- Returns:
```
{
    "deleted_movie": <movie_id>,
    "success": true
}
```

#### DELETE /actors
- General:
	Remove a movie from the database and returns the currently deleted actor's ID and a success value (True/False)
- Sample: `curl http://127.0.0.1:5000/actors/<actor_id>/ -X DELETE -H "Content-Type: application/json" "Authorization: Bearer {your token}"`

- Returns:
```
{
    "deleted_actor": <actor_id>,
    "success": true
}
```
