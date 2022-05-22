from flask import jsonify, request, make_response
from models import Event as EventModel, Person as PersonModel, db
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from config import Config
from datetime import datetime, timedelta


namespace = Namespace('auth', 'Auth endpoints')


@namespace.route('/login')
class Login(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Login')
    def post(self):
        auth = request.form
        if not auth or not auth.get('email') or not auth.get('password'):
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="Login required !!"'})

        user = PersonModel.query.filter_by(email=auth.get('email')).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'})

        if check_password_hash(user.password, auth.get('password')):
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, Config['SECRET_KEY'])

            return make_response(jsonify({'token': token.decode('UTF-8')}), 201)

        return make_response('Could not verify', 403, {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'})


@namespace.route('/signup')
class SingUp(Resource):

    @namespace.response(500, 'Internal Server error')
    @namespace.doc('SingUp')
    def post(self):
        input_data = request.form

        user = PersonModel.query.filter_by(email=input_data['email']).first()
        if not user:
            new_person = PersonModel(first_name=input_data['first_name'],
                                     second_name=input_data['second_name'],
                                     city_name=input_data['city_name'],
                                     address=input_data['address'],
                                     birth_day=input_data['birth_day'],
                                     email=input_data['email'],
                                     comment=input_data['comment'])
            new_person.set_password(input_data['password'])
            db.session.add(new_person)
            db.session.commit()
            return make_response('Successfully registered.', 201)
        else:
            return make_response('User already exists. Please Log in.', 202)