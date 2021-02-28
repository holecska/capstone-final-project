#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from sqlalchemy import exc

from ..database.models import setup_db, Movie, Actor
from ..auth.auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
setup_db(app)
CORS(app)

# ----------------------------------------------------------------------------
# CORS Headers
# ----------------------------------------------------------------------------
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

# APIs

# ----------------------------------------------------------------------------
# GET MOVIES
# ----------------------------------------------------------------------------

@app.route('/movies')
@requires_auth('get:elements')
def get_movies(jwt):

    movies = Movie.query.order_by(Movie.id).all()
    movies_formatted = [movie.format() for movie in movies]

    return jsonify({
        'success': True,
        'movies': movies_formatted
    })

# ----------------------------------------------------------------------------
# GET ACTORS
# ----------------------------------------------------------------------------

@app.route('/actors')
@requires_auth('get:elements')
def get_actors(jwt):

    actors = Actor.query.order_by(Actor.id).all()
    actor_formatted = [actor.format() for actor in actors]

    return jsonify({
        'success': True,
        'actor': actor_formatted
    })


# ----------------------------------------------------------------------------
# ADD MOVIES
# ----------------------------------------------------------------------------

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movies(jwt):

    body = request.get_json()
    title = body.get('title')
    release_date = body.get('release')

    try:
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
    except exc.IntegrityError:
        raise IntegrityErrorRaised(
        'A movie has an unique title! - It already exist')

    return jsonify({
        'success': True,
        'movie': movie.format()
    })

# ----------------------------------------------------------------------------
# ADD ACTORS
# ----------------------------------------------------------------------------

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actors(jwt):

    body = request.get_json()
    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    actor = Actor(name=name, age=age, gender=gender)
    actor.insert()

    return jsonify({
        'success': True,
        'actor': actor.format()
    })

# ----------------------------------------------------------------------------
# PATCH MOVIES
# ----------------------------------------------------------------------------

@app.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movies(jwt, id):

    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if movie is None:
        abort(404)

    body = request.get_json()

    for key in body:
        if hasattr(movie, key):
            setattr(movie, key, body[key])
        else:
            raise AttributeErrorRaised(
            'You are trying to modify an attribute which does not exist')

    movie.update()

    return jsonify({
        'success': True,
        'changed_movie': movie.id
    })

# ----------------------------------------------------------------------------
# PATCH ACTORS
# ----------------------------------------------------------------------------

@app.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actors(jwt, id):

    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None:
        abort(404)

    body = request.get_json()

    for key in body:
        if hasattr(actor, key):
            setattr(actor, key, body[key])
        else:
            raise AttributeErrorRaised(
            'You are trying to modify an attribute which does not exist')

    actor.update()

    return jsonify({
        'success': True,
        'changed_actor': actor.id
    })

# ----------------------------------------------------------------------------
# DELETE ACTORS
# ----------------------------------------------------------------------------
@app.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, id):

    actor = Actor.query.filter(Actor.id == id).one_or_none()

    if actor is None:
        abort(404)

    actor.delete()

    return jsonify({
        'success': True,
        'deleted_actor': actor.id
    })

# ----------------------------------------------------------------------------
# DELETE MOVIES
# ----------------------------------------------------------------------------
@app.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, id):

    movie = Movie.query.filter(Movie.id == id).one_or_none()

    if movie is None:
        abort(404)

    movie.delete()

    return jsonify({
        'success': True,
        'deleted_movie': movie.id
    })
# ----------------------------------------------------------------------------
# Error Handling
# ----------------------------------------------------------------------------


class IntegrityErrorRaised(Exception):

    def __init__(self, error_message="An error has occured, try it again!"):
        self.message = error_message


'''
Example error handling for unprocessable entity
'''

@app.errorhandler(IntegrityErrorRaised)
def integrity_problem(error):

    return jsonify({
        "success": False,
        "error": 422,
        "message": error.message
    }), 422

class AttributeErrorRaised(Exception):

    def __init__(self, error_message="An error has occured, try it again!"):
        self.message = error_message


'''
Example error handling for unprocessable entity
'''

@app.errorhandler(AttributeErrorRaised)
def attr_problem(error):

    return jsonify({
        "success": False,
        "error": 422,
        "message": error.message
    }), 422

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "ressource not found"
    }), 404


@app.errorhandler(405)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(AuthError)
def auth_error(AuthError):
    return jsonify({
        "success": False,
        "error": AuthError.status_code,
        "message": AuthError.error
    }), AuthError.status_code
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
