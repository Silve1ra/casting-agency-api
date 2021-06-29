import os
from flask import Flask, jsonify, render_template, abort, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from models import setup_db, Actor, Movie
from helpers import paginate_items
from auth import AuthError, requires_auth


def create_app():
    app = Flask(__name__, static_url_path='/static')
    setup_db(app)

    #  CORS
    #  ----------------------------------------------------------------

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')

        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, PATCH, POST, DELETE, OPTIONS')

        return response

    #  System
    #  ----------------------------------------------------------------

    @app.route('/')
    def index():
        return jsonify({
            'service': 'Casting Agency API',
            'version': '1.1',
            'author': 'Felipe Silveira'
        })

    @app.route('/docs')
    def documentation():
        return render_template('index.html')

    #  Actors
    #  ----------------------------------------------------------------

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            selection = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_items(request, selection)

            return jsonify({
                'error': False,
                'data': current_actors,
                'total_items': len(selection),
            })
        except BaseException:
            abort(400)

    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def show_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            return jsonify({
                'error': False,
                'data': actor.serialize(),
            })
        except BaseException:
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if 'name' not in body:
            abort(400)

        try:
            actor = Actor(
                name=body.get('name'),
                age=body.get('age'),
                gender=body.get('gender'))
            actor.insert()

            return jsonify({
                'error': False,
                'data': actor.serialize(),
            })
        except BaseException:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        try:
            if 'name' in body:
                actor.name = body.get('name')

            if 'age' in body:
                actor.age = body.get('age')

            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'error': False,
                'data': actor.serialize(),
            })

        except BaseException:
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            actor.delete()
            return jsonify({
                'error': False,
                'deleted': actor_id
            })

        except BaseException:
            abort(422)

    #  Movies
    #  ----------------------------------------------------------------

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            selection = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_items(request, selection)

            return jsonify({
                'error': False,
                'data': current_movies,
                'total_items': len(selection),
            })
        except BaseException:
            abort(400)

    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def show_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            return jsonify({
                'error': False,
                'data': movie.serialize(),
            })

        except BaseException:
            abort(404)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if 'title' not in body:
            abort(400)

        try:
            movie = Movie(
                title=body.get('title'),
                release_date=body.get('release_date'))
            movie.insert()

            return jsonify({
                'error': False,
                'data': movie.serialize(),
            })

        except BaseException:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()
        if not body:
            abort(400)

        try:
            if 'title' in body:
                movie.title = body.get('title')

            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()

            return jsonify({
                'error': False,
                'data': movie.serialize(),
            })

        except BaseException:
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.delete()
            return jsonify({
                'error': False,
                'deleted': movie_id
            })

        except BaseException:
            abort(422)

    #  Error handlers
    #  ----------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'unathorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
