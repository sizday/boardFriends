from app import db
from uuid import uuid4
from utils.GUID import GUID


games_compilation = db.Table('games_compilation',
                             db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                             db.Column('game_id', db.Integer, db.ForeignKey('game.id')))

participation = db.Table('participation',
                         db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                         db.Column('person_id', db.Integer, db.ForeignKey('person.id')))

favorite_games = db.Table('favorite_games',
                          db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
                          db.Column('games_id', db.Integer, db.ForeignKey('game.id')))


class Event(db.Model):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid4()))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    time = db.Column(db.Time)
    max_player = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    games_compilation = db.relationship('Game', secondary=games_compilation,
                                        backref=db.backref('events', lazy='dynamic'))
    participation = db.relationship('Person', secondary=participation,
                                    backref=db.backref('participation', lazy='dynamic'))

    def __repr__(self):
        string = f"Place: {self.place_id}, Time: {self.time}\n" \
                 f"Creator: {self.creator_id} MaxCountPlayer: {self.max_player}\n" \
                 f"Comment: {self.comment}"
        return string


class Person(db.Model):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid4()))
    first_name = db.Column(db.String(255))
    second_name = db.Column(db.String(255))
    city_name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    birth_day = db.Column(db.Date)
    favorite_games = db.relationship('Game', secondary=favorite_games,
                                     backref=db.backref('favorite_games', lazy='dynamic'))
    creating = db.relationship('Event', backref='creator', uselist=False)


class Game(db.Model):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255))
    genre = db.Column(db.String(50))
    difficult = db.Column(db.Integer)
    themes = db.Column(db.String(50))


class Place(db.Model):
    id = db.Column(GUID(), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    address = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    events = db.relationship('Event', backref='place', uselist=False)


db.drop_all()
db.create_all()
