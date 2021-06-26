import os
from flask import Flask, jsonify, render_template, abort, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer

app = Flask(__name__, static_url_path='/static')

#  CORS
#  ----------------------------------------------------------------

CORS(app)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

#  Db config
#  ----------------------------------------------------------------

database_path = os.environ['DATABASE_URL']
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# db.init_app(app)

#  Model
#  ----------------------------------------------------------------

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

db.app = app
db.create_all()

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
    

if __name__ == '__main__':
    app.run()