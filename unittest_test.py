import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from backend.database.models import setup_db


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
                                                            'postgres',
                                                            'admin',
                                                            'localhost:5432',
                                                            self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    default_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBfVnJpcDNjMl91R093UVluQkp0SSJ9.eyJpc3MiOiJodHRwczovL2hvbGVjc2thLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDM2YTEwYjg1MzY3NTAwNmZkZTZlOGIiLCJhdWQiOiJjYXBzdG9uZV9pZGVudGlmaWVyIiwiaWF0IjoxNjE0MzY3NTI0LCJleHAiOjE2MTQzNzQ3MjQsImF6cCI6InFoREpWNzBzdlZjTm5qUmtIVVV0eHFPRHlGcXoxbFRKIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZWxlbWVudHMiXX0.Q7Ntd2uehEtbLeSAuRn6PPRJjRiNtQ7OIraQrJk7TCyMng8HlSKWfz9uEhdwCs6mwN7V-1t_lBOTswKKlEjdUZKYTfx1J5Sq4sF5fyO-CdnmKTa5lXdlb2vesD3DXWM037lrM-LNHhl2kWcsxbkK1_mJ0Mh_9bQO5aGWGm1r1bKjV_S1WbEl_U5txJN6jzMUD3tuR1VrGyQpxbdVeiQoaZkmcwMP4n2_BXkIYTaGuAz7CNjd0eEKGIxmObtqXkbvMVgOuM0LoAThfgWQgcoXnfFM-v-YX4uP8cZhYT8sgd3K0WoF5NzvkNAQBYpZOFrMK866_RSh9HjAw-4ZoMSMLQ"

    def auth(self, token=default_token):
        auth_token = "Bearer " + token

        header_json = {
            "Content-Type": "application/json",
            "Authorization": auth_token
        }

        return header_json

    # TEST EXPIRED TOKEN
    def test_expired_token(self):
        json_header = self.auth()
        res = self.client().get('/movies', headers=json_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        schema = {
            "message": {
              "code": "token_expired",
              "description": "Token expired."
            }
        }
        self.assertDictContainsSubset(schema, data)
        self.assertEqual(data['success'], False)

    # CASTING Assistant
    token_assistant = os.getenv('token_assistant')

    # Test for get method - movies
    def test_assistant_get_movies(self):
        json_header = self.auth(CapstoneTestCase.token_assistant)
        res = self.client().get('/movies', headers=json_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for get method - movies
    def test_assistant_get_actors(self):
        json_header = self.auth(CapstoneTestCase.token_assistant)
        res = self.client().get('/actors', headers=json_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # CASTING Director
    token_director = os.getenv('token_director')

    actor_id = None

    # Test for POST new actor
    def test_director_a_post_actors(self):
        json_header = self.auth(CapstoneTestCase.token_director)
        body = {
                "name": "Joaquin Phoenix",
                "age": 46,
                "gender": "men"
        }
        res = self.client().post('/actors', headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
            "actor":
                {
                    "age": 46,
                    "gender": "men",
                    "id": data['actor']['id'],
                    "name": "Joaquin Phoenix"
                },
            "success": True
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertDictContainsSubset(schema, data)
        CapstoneTestCase.actor_id = data['actor']['id']

    # Test for PATCH existing actor
    def test_director_b_patch_actor(self):
        json_header = self.auth(CapstoneTestCase.token_director)
        body = {
                "age": 47
        }
        act_id = CapstoneTestCase.actor_id
        res = self.client().patch('/actors/' + str(act_id),
                                  headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
            "changed_actor": act_id,
            "success": True
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test Error - if not existing attr should be changed
    def test_director_b_patch_actor_attr_err(self):
        json_header = self.auth(CapstoneTestCase.token_director)
        body = {
                "title": "New Film"
        }
        act_id = CapstoneTestCase.actor_id
        res = self.client().patch('/actors/' + str(act_id),
                                  headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
            "error": 422,
            "message": ("You are trying to modify an attribute which does not "
                        "exist"),
            "success": False
        }
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertDictContainsSubset(schema, data)

    # Test for Role Error - Assistant not allowed to change actor
    def test_director_b_patch_actor_role_err(self):
        json_header = self.auth(CapstoneTestCase.token_assistant)
        body = {
                "age": 47
        }
        act_id = CapstoneTestCase.actor_id
        res = self.client().patch('/actors/' + str(act_id),
                                  headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
                    "error": 401,
                    "message": {
                        "code": "forbidden",
                        "description": ("Permission not found. - method not "
                                        "allowed")
                    },
                    "success": False
                }
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertDictContainsSubset(schema, data)

    # Test for DELETE an actor
    def test_director_c_delete_actor(self):
        json_header = self.auth(CapstoneTestCase.token_director)
        act_id = CapstoneTestCase.actor_id
        res = self.client().delete('/actors/' + str(act_id),
                                   headers=json_header)
        data = json.loads(res.data)
        schema = {
            "deleted_actor": act_id,
            "success": True
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for POST new movie - ERROR Role Test, Director not allowed
    def test_director_post_movie(self):
        json_header = self.auth(CapstoneTestCase.token_director)
        body = {
                "title": "Joker",
                "release_date": "2019.05.17"
        }
        res = self.client().post('/movies', headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
                    "error": 401,
                    "message": {
                        "code": "forbidden",
                        "description": ("Permission not found. - method not "
                                        "allowed")
                    },
                    "success": False
                }
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertDictContainsSubset(schema, data)

    # Executive Producer
    token_producer = os.getenv('token_producer')

    movie_id = None

    # Test for POST new movie
    def test_producer_a_post_movie_a(self):
        json_header = self.auth(CapstoneTestCase.token_producer)
        body = {
                "title": "Joker",
                "release_date": "2019.10.03"
        }
        res = self.client().post('/movies', headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
                    "movie": {
                        "id": data['movie']['id'],
                        "release_date": "Thu, 03 Oct 2019 00:00:00 GMT",
                        "title": "Joker"
                    },
                    "success": True
                }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertDictContainsSubset(schema, data)
        CapstoneTestCase.movie_id = data['movie']['id']

    # Test for POST new movie - ERROR unique Title
    def test_producer_a_post_movie_b(self):
        json_header = self.auth(CapstoneTestCase.token_producer)
        body = {
                "title": "Joker",
                "release_date": "2019.05.17"
        }
        res = self.client().post('/movies', headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
            "error": 422,
            "message": "A movie has an unique title! - It already exist",
            "success": False
        }
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertDictContainsSubset(schema, data)

    # Test for PATCH existing actor
    def test_producer_b_patch_movie(self):
        json_header = self.auth(CapstoneTestCase.token_producer)
        body = {
                "title": "Joker New Episode"
        }
        mov_id = CapstoneTestCase.movie_id
        res = self.client().patch('/movies/' + str(mov_id),
                                  headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
            "changed_movie": mov_id,
            "success": True
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test PATCH Movie by director
    def test_producer_b_patched_movie_director(self):
        json_header = self.auth(CapstoneTestCase.token_director)
        body = {
                "title": "Joker New Episode by Director"
        }
        mov_id = CapstoneTestCase.movie_id
        res = self.client().patch('/movies/' + str(mov_id),
                                  headers=json_header, json=body)
        data = json.loads(res.data)
        schema = {
            "changed_movie": mov_id,
            "success": True
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test for DELETE a movie
    def test_producer_c_delete_movie(self):
        json_header = self.auth(CapstoneTestCase.token_producer)
        mov_id = CapstoneTestCase.movie_id
        res = self.client().delete('/movies/' + str(mov_id),
                                   headers=json_header)
        data = json.loads(res.data)
        schema = {
            "deleted_movie": mov_id,
            "success": True
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
