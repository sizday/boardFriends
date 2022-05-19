from flask import request
from models import Game as GameModel, db
from flask_restx import Namespace, Resource, fields

namespace = Namespace('games', 'Games endpoints')

game_model = namespace.model('Game', {
    'id': fields.Integer(
        readonly=True,
        description='Game identifier'
    ),
    'name': fields.String(
        required=True,
        description='Game name'
    ),
    'genre': fields.String(
        required=True,
        description='Game genre'
    ),
    'difficult': fields.Integer(
        required=True,
        description='Game difficult'
    ),
    'themes': fields.String(
        required=True,
        description='Game themes'
    )
})


@namespace.route('')
class Games(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('List games')
    @namespace.marshal_with(game_model)
    def get(self):
        games = GameModel.query.all()
        return games

    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Create new game')
    @namespace.marshal_with(game_model, code=201)
    @namespace.expect(game_model, validate=True)
    def post(self):
        input_data = request.get_json()
        new_game = GameModel(name=input_data['name'],
                             genre=input_data['genre'],
                             difficult=input_data['difficult'],
                             themes=input_data['themes'])
        db.session.add(new_game)
        db.session.commit()
        return new_game


@namespace.route('/<int:game_id>')
class Game(Resource):
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Find game by ID')
    @namespace.marshal_with(game_model)
    def get(self, game_id):
        game = GameModel.query.filter_by(id=game_id).first()
        return game
