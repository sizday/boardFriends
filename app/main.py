from flask import Flask
from config import Config
from models import db, Person, authenticate, identity
from flask_login import LoginManager
from flask_migrate import Migrate
from blueprints import blueprint as basic_endpoints
from flask_jwt import JWT
import jwt

app = Flask(__name__)

app.config.from_object(Config)
app.register_blueprint(basic_endpoints)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()


# db.drop_all()
db.create_all()
db.session.commit()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
