from flask import Flask
from config import Config
from models import db
from blueprints import blueprint as basic_endpoints

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(basic_endpoints)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.app_context().push()
# db.drop_all()
db.create_all()
db.session.commit()

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
