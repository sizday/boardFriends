from flask import request
from app.models import Person as PersonModel, db
from flask_restplus import Namespace, Resource, fields

namespace = Namespace('persons', 'Person endpoints')

person_model = namespace.model('Person', {
    'id': fields.String(
        readonly=True,
        description='Person identifier'
    ),
    'first_name': fields.String(
        required=True,
        description='First name of person'
    ),
    'second_name': fields.String(
        required=True,
        description='Second name of person'
    ),
    'city_name': fields.String(
        required=True,
        description='City name of living person'
    ),
    'address': fields.String(
        required=True,
        description='Address of living person'
    ),
    'birth_day': fields.String(
        required=True,
        description='Birthday of person'
    ),
    'password': fields.String(
        required=True,
        description='Password of person'
    ),
    'email': fields.String(
        required=True,
        description='EMail of person'
    ),
    'comment': fields.String(
        required=True,
        description='About person'
    ),
})


@namespace.route('')
class Persons(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('List persons')
    @namespace.marshal_list_with(person_model)
    def get(self):
        persons = PersonModel.query.all()
        return persons

    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Create new person')
    @namespace.marshal_with(person_model, code=201)
    @namespace.expect(person_model, validate=True)
    def post(self):
        input_data = request.get_json()
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
        return new_person


@namespace.route('/<person_id>')
class Person(Resource):
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Find event by ID')
    @namespace.marshal_with(person_model)
    def get(self, person_id):
        person = PersonModel.query.filter_by(id=person_id).first()
        return person

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Update person data')
    @namespace.expect(person_model, validate=True)
    @namespace.marshal_with(person_model)
    def put(self, person_id):
        person = PersonModel.query.filter_by(id=person_id).first()
        input_data = request.get_json()
        person.first_name = input_data['first_name']
        person.second_name = input_data['second_name']
        person.city_name = input_data['city_name']
        person.address = input_data['address']
        person.birth_day = input_data['birth_day']
        person.email = input_data['email']
        person.comment = input_data['comment']
        db.session.commit()
        return person

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Delete person')
    @namespace.marshal_with(person_model)
    def delete(self, person_id):
        person = PersonModel.query.filter_by(id=person_id).first()
        db.session.delete(person)
        db.session.commit()
        return person
