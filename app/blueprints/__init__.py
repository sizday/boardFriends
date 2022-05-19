from flask import Blueprint
from flask_restplus import Api
from app.blueprints.games import namespace as games_ns
from app.blueprints.events import namespace as events_ns
from app.blueprints.persons import namespace as person_ns

async_mode = None
thread = None
blueprint = Blueprint('api', __name__, url_prefix='/api')

api_extension = Api(
    blueprint,
    title='Flask REST',
    version='1.0',
    description='API BoardFriends',
    doc='/doc'
)

api_extension.add_namespace(games_ns)
api_extension.add_namespace(events_ns)
api_extension.add_namespace(person_ns)
