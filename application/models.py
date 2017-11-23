from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#Flask app configurations
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = b'\xeev\xc5\xe0\x0c9\x94\x1f\xad\xff\x02\xc2\xaa_bx\x0e\xf3*\x05\x01"\x02:'
# Flask-SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aagsport.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

#object for each athlete
class Athlete(db.Model):
    __tablename__ = "athletes"
    Lname = db.Column(db.String(50))
    Fname = db.Column(db.String(50))
    Gradyear = db.Column(db.Integer)
    ath_ID = db.Column(db.Integer, primary_key=True)

    def __init__(self, lastname, firstname, gradyear, ath_ID):
        self.Lname = lastname
        self.Fname = firstname
        self.Gradyear = gradyear
        self.ath_ID = ath_ID

#object for each coach
class Coach(db.Model):
    __tablename__ = "coaches"
    Lname = db.Column(db.String(50))
    Fname = db.Column(db.String(50))
    coach_ID = db.Column(db.Integer, primary_key=True)

    def __init__(self, lastname, firstname, coach_ID):
        self.Lname = lastname
        self.Fname = firstname
        self.coach_ID = coach_ID

#object for every photo, information for every picture
class Photo(db.Model):
    __tablename__ = "photos"
    year = db.Column(db.Integer)
    filename = db.Column(db.String(50))
    sport_ID = db.Column(db.Integer)
    pic_ID = db.Column(db.Integer, primary_key=True)

    def __init__(self, year, filename, sport_ID, pic_ID):
        self.year = year
        self.filename = filename
        self.sport_ID = sport_ID
        self.pic_ID = pic_ID

#lists everyone in a photo, includes no description of rows
class Photo_seat(db.Model):
    __tablename__ = "photo_seating"
    pic_ID = db.Column(db.Integer)
    row_ID = db.Column(db.Integer)
    ath_ID = db.Column(db.Integer)
    coach_ID = db.Column(db.Integer)
    seat_ID = db.Column(db.Integer, primary_key=True)
    
    def __init__(self, pic_ID, row_ID, ath_ID, coach_ID, seat_ID):
        self.pic_ID = pic_ID
        self.row_ID = row_ID
        self.ath_ID = ath_ID
        self.coach_ID = coach_ID
        self.seat_ID = seat_ID

#row descriptions ONLY, no people are listed here
class Row(db.Model):
    __tablename__ = "rows"
    pic_ID = db.Column(db.Integer)
    row_desc = db.Column(db.String(250))
    row_ID = db.Column(db.Integer, primary_key=True)

    def __init__(self, pic_ID, row_desc, row_ID):
        self.pic_ID = pic_ID
        self.row_desc = row_desc
        self.row_ID = row_ID

class Sport(db.Model):
    __tablename__ = "sports"
    sport_name = db.Column(db.String(50))
    sport_ID = db.Column(db.Integer, primary_key=True)

    def __init__(self, sport_name, sport_ID):
        self.sport_name = sport_name
        self.sport_ID = sport_ID
