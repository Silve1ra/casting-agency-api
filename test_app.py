import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie

# Auth Roles.
#  ----------------------------------------------------------------

JWT_CASTING_ASSISTANT = os.environ.get('ASSISTANT')
JWT_CASTING_DIRECTOR = os.environ.get('DIRECTOR')
JWT_EXECUTIVE_PRODUCER = os.environ.get('PRODUCER')


class CastingAgencyTestCase(unittest.TestCase):
    print(JWT_CASTING_ASSISTANT)
    print(JWT_CASTING_DIRECTOR)
    print(JWT_EXECUTIVE_PRODUCER)

    # Db Config.
    #  ----------------------------------------------------------------

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

    # Unit tests.
    #  ----------------------------------------------------------------

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

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)

    def test_404_create_actor(self):
        new_actor = {
            "age": 20,
            "gender": "female"
        }

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_DIRECTOR})
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
        res = self.client().patch(
            url, json=updated_actor, headers={
                "Authorization": "Bearer " + JWT_CASTING_DIRECTOR})
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
        res = self.client().patch(
            url, json=updated_actor, headers={
                "Authorization": "Bearer " + JWT_CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        actor_id = 1
        url = '/actors/' + str(actor_id)
        res = self.client().delete(
            url,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['deleted'], actor_id)

    def test_404_delete_actor(self):
        actor_id = 999
        url = '/actors/' + str(actor_id)
        res = self.client().delete(
            url,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_DIRECTOR})
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
        res = self.client().patch(
            url, json=updated_movie, headers={
                "Authorization": "Bearer " + JWT_CASTING_DIRECTOR})
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
        res = self.client().patch(
            url, json=updated_movie, headers={
                "Authorization": "Bearer " + JWT_CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        movie_id = 1
        url = '/movies/' + str(movie_id)
        res = self.client().delete(
            url,
            headers={
                "Authorization": "Bearer " +
                JWT_EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], False)
        self.assertEqual(data['deleted'], movie_id)

    def test_404_delete_movie(self):
        movie_id = 999
        url = '/movies/' + str(movie_id)
        res = self.client().delete(
            url,
            headers={
                "Authorization": "Bearer " +
                JWT_EXECUTIVE_PRODUCER})
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

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_create_movie(self):
        new_movie = {
            "title": "test",
            "release_date": "2000-01-20"
        }

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_ASSISTANT})
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
        res = self.client().patch(
            url,
            json=updated_actor,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_ASSISTANT})
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
        res = self.client().patch(
            url,
            json=updated_movie,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_delete_actor(self):
        actor_id = 1
        url = '/actors/' + str(actor_id)
        res = self.client().delete(
            url,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_assistant_delete_movie(self):
        movie_id = 1
        url = '/movies/' + str(movie_id)
        res = self.client().delete(
            url,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_ASSISTANT})
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

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)

    def test_401_director_delete_movie(self):
        movie_id = 1
        url = '/movies/' + str(movie_id)
        res = self.client().delete(
            url,
            headers={
                "Authorization": "Bearer " +
                JWT_CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['message'], "Unathorized.")
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
