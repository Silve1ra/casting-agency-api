import os
from flask import Flask, jsonify, render_template, abort, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from models import setup_db, Actor, Movie

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
    selection = Actor.query.all()
    actors = [item.serialize() for item in selection]

    return jsonify({
        'actors': actors,
        'error': False
    })
    
@app.route('/movies')
def get_movies():
    selection = Movie.query.all()
    movies = [item.serialize() for item in selection]

    return jsonify({
        'movies': movies,
        'error': False
    })

if __name__ == '__main__':
    app.run()