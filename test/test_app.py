#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app_test import create_app
from models_test import setup_db, db_drop_and_create_all, Actor, Movie

#----------------------------------------------------------------------------#
# Auth Roles.
#----------------------------------------------------------------------------#
JWT_CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBtRXg1YzJ2TmVyaE15RHB4VFB5NiJ9.eyJpc3MiOiJodHRwczovL3NpbHZlMXJhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGQ1MjhjYmYzNWU0MjAwNzE5YjhhNTUiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNDgzNDU0MywiZXhwIjoxNjI0OTIwOTQzLCJhenAiOiJtN3hqVE00WTJTcUdmTFJrOVk3aFRjcjhCYnhjaWZiVSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Gi5TalwpoVBF9BdrgYKwCXuVEMhz6MfWAwo07fNW9-t0b5_RIFChKHY6URWAUeUVemPN-ThRlGOT9RJLEy_dOceoqw_U9H65Vf3_fChpgR0leWGDFhqeQWQkiToNT0Kmwpy3C50JreyN-_m30-crEpZYH_vLUhKxrLethfT4cW_DaEpEpMGFn3WshkEGl3mFy0jtmDRGcjEOU7t8a_YoL8pUULDuIOLKhvDnHGEX08fBvDstQ_uPs_CVle5B4XAne5u91vyNq2jbj1IfpW1fcEmM6F22dpIix3XbagVKiQ0qfG7uywU5WXrxbQEG4Yzvk_E9R-6pLzJtsBqoCNpjvg'

JWT_CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBtRXg1YzJ2TmVyaE15RHB4VFB5NiJ9.eyJpc3MiOiJodHRwczovL3NpbHZlMXJhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGQ1MjkxMWMwYjgwYTAwNmE4MmMyNTYiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNDgzNDU4NCwiZXhwIjoxNjI0OTIwOTg0LCJhenAiOiJtN3hqVE00WTJTcUdmTFJrOVk3aFRjcjhCYnhjaWZiVSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.YWRYaz47nTinK26_UinIG7oygpTftEXfHINFTpb6CKsRlzMoAH9xIkljXsu_dqatqm2ZVmTVMlRFGLtyWUPKZgMERfoBOeMPJMtPjnShMUYJ-c56appX-E4L2GQyOyFx6APFKR2hxPtn_1pdvxpa_XozeczzCr3LxI45RVLfKhWX16Iu4PkwqshO1HDcO6K06p7YIpB6-DIa1yODeSY2H7sP5eLGix5Q9a8VqHy9jroj6P78vPWwFnRs__bXBKjppUnVg0o5XYqy5d9WL_Lxzh7057ELGtxvNef9O5bnRgWNLrX2cVYaH7_6fqgKqgETan0Lcr38dr6pZvSsLNQhFQ'

JWT_EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBtRXg1YzJ2TmVyaE15RHB4VFB5NiJ9.eyJpc3MiOiJodHRwczovL3NpbHZlMXJhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MGQ1Mjk2MmZiMTQ2ZjAwNjkwNTI4NWQiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNDgzNDYyMSwiZXhwIjoxNjI0OTIxMDIxLCJhenAiOiJtN3hqVE00WTJTcUdmTFJrOVk3aFRjcjhCYnhjaWZiVSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.YBpJNpFZpwLdzqgwy1NpyW5wNWTvNi958SULsdZY-XEx_UdzSdM4P1EbmPOpSpo_SADLCTLS5ElCaPqMgEe0ONWw5q49YRj0EddAaZdgmpchiQMTFsDfQc-rPb0zoBoZIETY-9ryLiXxX1xb0jTCyjijn8Q3Q-nBxPUV82oXvoF2PvvGirwCs5-iMktKC-EknGL74V57cjrA9W6cMLbPlbqPcd3jeC2OAgtLo_Jji2o1IXnvBOAjXUJ7SK-2zpnAKcanIylhB_DLghpG3gYm301Tf_vSoIA3jNLmeox1FLXX_CAjqFRaTAm43iMhN5-oCKUrO5xCtx6dumV_dz8fMw'


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    #----------------------------------------------------------------------------#
    # Db Config.
    #----------------------------------------------------------------------------#

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    #----------------------------------------------------------------------------#
    # Unit tests.
    #----------------------------------------------------------------------------#

    #  Actor
    #  ----------------------------------------------------------------

    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer " +
                                    JWT_CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_show_actor(self):
        res = self.client().get('/actors/1',
                                headers={
                                    "Authorization": "Bearer " +
                                    JWT_CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_404_show_actor(self):
        res = self.client().get('/actors/999',
                                headers={
                                    "Authorization": "Bearer " +
                                    JWT_CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_actor(self):
        new_actor = {
            "name": "test",
            "age": 20,
            "gender": "female"
        }

        res = self.client().post('/actors', json=new_actor,
                                 headers={
                                     "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_404_create_actor(self):
        new_actor = {
            "age": 20,
            "gender": "female"
        }

        res = self.client().post('/actors', json=new_actor,
                                 headers={
                                     "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_actor(self):
        actor_id = 1
        updated_actor = {
            "name": "test update",
            "age": 20,
            "gender": "female"
        }

        url = '/actors/' + str(actor_id)
        res = self.client().patch(url, json=updated_actor,
                                  headers={
                                      "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_404_update_actor(self):
        actor_id = 999
        updated_actor = {
            "name": "test update",
            "age": 20,
            "gender": "female"
        }

        url = '/actors/' + str(actor_id)
        res = self.client().patch(url, json=updated_actor,
                                  headers={
                                      "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        actor_id = 1
        url = '/actors/' + str(actor_id)
        res = self.client().delete(url,
                                   headers={
                                       "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['deleted'], actor_id)

    def test_404_delete_actor(self):
        actor_id = 999
        url = '/actors/' + str(actor_id)
        res = self.client().delete(url,
                                   headers={
                                       "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    #  Movie
    #  ----------------------------------------------------------------

    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer " +
                                    JWT_CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_show_movie(self):
        res = self.client().get('/movies/1',
                                headers={
                                    "Authorization": "Bearer " +
                                    JWT_CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_404_show_movie(self):
        res = self.client().get('/movies/999',
                                headers={
                                    "Authorization": "Bearer " +
                                    JWT_CASTING_ASSISTANT}
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_movie(self):
        new_movie = {
            "title": "test",
            "release_date": "2000-01-20"
        }

        res = self.client().post('/movies', json=new_movie,
                                 headers={
                                     "Authorization": "Bearer " +
                                     JWT_EXECUTIVE_PRODUCER}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_404_create_movie(self):
        new_movie = {
            "age": 20,
            "gender": "female"
        }

        res = self.client().post('/movies', json=new_movie,
                                 headers={
                                     "Authorization": "Bearer " +
                                     JWT_EXECUTIVE_PRODUCER}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_movie(self):
        movie_id = 1
        updated_movie = {
            "name": "test update",
            "age": 20,
            "gender": "female"
        }

        url = '/movies/' + str(movie_id)
        res = self.client().patch(url, json=updated_movie,
                                  headers={
                                      "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_404_update_movie(self):
        movie_id = 999
        updated_movie = {
            "name": "test update",
            "age": 20,
            "gender": "female"
        }

        url = '/movies/' + str(movie_id)
        res = self.client().patch(url, json=updated_movie,
                                  headers={
                                      "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        movie_id = 1
        url = '/movies/' + str(movie_id)
        res = self.client().delete(url,
                                   headers={
                                       "Authorization": "Bearer " + JWT_EXECUTIVE_PRODUCER}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['deleted'], movie_id)

    def test_404_delete_movie(self):
        movie_id = 999
        url = '/movies/' + str(movie_id)
        res = self.client().delete(url,
                                   headers={
                                       "Authorization": "Bearer " + JWT_EXECUTIVE_PRODUCER}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    #  RBAC
    #  ----------------------------------------------------------------

    '''
        Casting Assistant cannot create, update or delete actors and/or movies
    '''

    def test_401_assistant_create_actor(self):
        new_actor = {
            "name": "test",
            "age": 20,
            "gender": "female"
        }

        res = self.client().post('/actors', json=new_actor,
                                 headers={
                                     "Authorization": "Bearer " + JWT_CASTING_ASSISTANT}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_create_movie(self):
        new_movie = {
            "title": "test",
            "release_date": "2000-01-20"
        }

        res = self.client().post('/movies', json=new_movie,
                                 headers={
                                     "Authorization": "Bearer " + JWT_CASTING_ASSISTANT}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_update_actor(self):
        actor_id = 1
        updated_actor = {
            "name": "test update",
            "age": 20,
            "gender": "female"
        }

        url = '/actors/' + str(actor_id)
        res = self.client().patch(url, json=updated_actor,
                                  headers={
                                      "Authorization": "Bearer " + JWT_CASTING_ASSISTANT}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_update_movie(self):
        movie_id = 1
        updated_movie = {
            "name": "test update",
            "age": 20,
            "gender": "female"
        }

        url = '/movies/' + str(movie_id)
        res = self.client().patch(url, json=updated_movie,
                                  headers={
                                      "Authorization": "Bearer " + JWT_CASTING_ASSISTANT}
                                  )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_delete_actor(self):
        actor_id = 1
        url = '/actors/' + str(actor_id)
        res = self.client().delete(url,
                                   headers={
                                       "Authorization": "Bearer " + JWT_CASTING_ASSISTANT}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_delete_movie(self):
        movie_id = 1
        url = '/movies/' + str(movie_id)
        res = self.client().delete(url,
                                   headers={
                                       "Authorization": "Bearer " + JWT_CASTING_ASSISTANT}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    '''
        Casting Director cannot create or delete movies
    '''

    def test_401_director_create_movie(self):
        new_movie = {
            "title": "test",
            "release_date": "2000-01-20"
        }

        res = self.client().post('/movies', json=new_movie,
                                 headers={
                                     "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                 )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_director_delete_movie(self):
        movie_id = 1
        url = '/movies/' + str(movie_id)
        res = self.client().delete(url,
                                   headers={
                                       "Authorization": "Bearer " + JWT_CASTING_DIRECTOR}
                                   )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
