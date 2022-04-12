from app import app
from flask import jsonify
from app.db_models import Place, Person, Event, Game

async_mode = None
thread = None


@app.route("/")
def index():
    return "Hello World!"


@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify({'events': events})


@app.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify({'games': games})


if __name__ == '__main__':
    app.run(debug=True)
