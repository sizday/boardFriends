from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256
from functools import wraps
from flask import request, jsonify, make_response
import jwt
from config import Config

db = SQLAlchemy()

games_compilation = db.Table('games_compilation',
                             db.Column('event_id', UUID(as_uuid=True), db.ForeignKey('event.id')),
                             db.Column('game_id', UUID(as_uuid=True), db.ForeignKey('game.id')))

participation = db.Table('participation',
                         db.Column('event_id', UUID(as_uuid=True), db.ForeignKey('event.id')),
                         db.Column('person_id', UUID(as_uuid=True), db.ForeignKey('person.id')))

favorite_games = db.Table('favorite_games',
                          db.Column('person_id', UUID(as_uuid=True), db.ForeignKey('person.id')),
                          db.Column('games_id', UUID(as_uuid=True), db.ForeignKey('game.id')))


class Event(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(255))
    place = db.Column(db.String(255))
    creator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('person.id'))
    time = db.Column(db.String(255))
    max_player = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    games_compilation = db.relationship('Game', secondary=games_compilation,
                                        backref=db.backref('games', lazy='dynamic'))
    participation = db.relationship('Person', secondary=participation,
                                    backref=db.backref('participation', lazy='dynamic'))

    def __repr__(self):
        string = f"Place: {self.place}, Time: {self.time}\n" \
                 f"Creator: {self.creator_id} MaxCountPlayer: {self.max_player}\n" \
                 f"Comment: {self.comment}"
        return string


class Person(UserMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(255))
    second_name = db.Column(db.String(255))
    city_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    birth_day = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    favorite_games = db.relationship('Game', secondary=favorite_games,
                                     backref=db.backref('favorite_games', lazy='dynamic'))
    creating = db.relationship('Event', backref='creator', uselist=False)

    def __repr__(self):
        string = f"Name: {self.first_name} {self.id}\nEmail: {self.email}\nCityName: {self.city_name}\n" \
                 f"Address: {self.address}\nBirthDay: {self.birth_day}"
        return string

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Game(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(255))
    genre = db.Column(db.String(50))
    difficult = db.Column(db.Integer)
    themes = db.Column(db.String(50))


class Place(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    address = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)


def authenticate(username, password):
    user = Person.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return Person.query.get(user_id)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, Config['SECRET_KEY'])
            current_user = Person.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated
