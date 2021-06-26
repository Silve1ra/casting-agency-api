import os
from flask import Flask, jsonify, render_template, abort, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from models import setup_db, Actor, Movie
from helpers import paginate_items

app = Flask(__name__, static_url_path='/static')
setup_db(app)

#  CORS
#  ----------------------------------------------------------------

CORS(app)


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
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

#  Actor
#  ----------------------------------------------------------------


@app.route('/actors')
def get_actors():
    try:
        selection = Actor.query.order_by(Actor.id).all()
        current_actors = paginate_items(request, selection)

        return jsonify({
            'error': False,
            'data': current_actors,
            'total_items': len(selection),
        })
    except BaseException:
        abort(422)


#  Movies
#  ----------------------------------------------------------------

@app.route('/movies')
def get_movies():
    try:
        selection = Movie.query.order_by(Movie.id).all()
        current_movies = paginate_items(request, selection)

        return jsonify({
            'error': False,
            'data': current_movies,
            'total_items': len(selection),
        })
    except BaseException:
        abort(422)


if __name__ == '__main__':
    app.run()
