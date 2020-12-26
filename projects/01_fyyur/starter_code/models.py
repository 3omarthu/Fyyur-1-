from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)



class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120),unique=True, nullable = False)
    image_link = db.Column(db.String(500), nullable = True)
    genres = db.Column(db.String(120), nullable = True)
    facebook_link = db.Column(db.String(120), nullable = True)
    website = db.Column(db.String(120), nullable = True)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), nullable = True)
    shows = db.relationship('Show', backref = 'Venue', lazy = True)
    
    
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120),unique=True, nullable = False)
    image_link = db.Column(db.String(500), nullable = True)
    genres = db.Column(db.String(120), nullable = True)
    facebook_link = db.Column(db.String(120), nullable = True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref = 'Artist', lazy = True)
    
    

    
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    start_time = db.Column(db.DateTime, nullable = False)
    venue = db.relationship('Venue')
    artist = db.relationship('Artist')
