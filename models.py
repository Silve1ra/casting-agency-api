from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/postgres'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    db.drop_all()
    db.create_all()

    insert_demo_data()
    

def insert_demo_data():
    # add one demo row for actors
    actor = Actor(
        name='Christian Bale',
        age='47',
        gender='male'
    )
    actor.insert()

    # add one demo row for movies
    movie = Movie(
        title='The Dark Knight Rises',
        release_date='2012-07-27',
    )
    movie.insert()

#  Actor
#  ----------------------------------------------------------------

class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return '<Actor created: ID %r>' % self.id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }


#  Movie
#  ----------------------------------------------------------------
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.DateTime(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return '<Movie created: ID %r>' % self.id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }
