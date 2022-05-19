from flask import jsonify, request
from models import Event as EventModel, Person as PersonModel, db
from flask_restx import Namespace, Resource, fields

namespace = Namespace('events', 'Games endpoints')


event_model = namespace.model('Event', {
    'id': fields.String(
        readonly=True,
        description='Game identifier'
    ),
    'place': fields.String(
        required=True,
        description='Place of event'
    ),
    'creator_id': fields.String(
        required=True,
        description='Creator ID'
    ),
    'time': fields.String(
        required=True,
        description='Time of event'
    ),
    'max_player': fields.Integer(
        required=True,
        description='Count of max player'
    ),
    'comment': fields.String(
        required=True,
        description='Comment for event'
    )
})

participation_model = namespace.model('Participation', {
    'person_id': fields.Integer(
        readonly=True,
        description='New player ID'
    )
})

unparticipation_model = namespace.model('Unparticipation', {
    'person_id': fields.Integer(
        readonly=True,
        description='Delete Player ID'
    ),
    'event_id': fields.Integer(
        readonly=True,
        description='Event ID'
    )
})


@namespace.route('')
class Events(Resource):
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('List events')
    @namespace.marshal_list_with(event_model)
    def get(self):
        events = EventModel.query.all()
        return events

    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Create new event')
    @namespace.marshal_with(event_model, code=201)
    @namespace.expect(event_model, validate=True)
    def post(self):
        input_data = request.get_json()
        new_event = EventModel(creator=input_data['creator_id'],
                               place=input_data['place'],
                               time=input_data['time'],
                               max_player=input_data['max_player'],
                               comment=input_data['comment'])
        db.session.add(new_event)
        db.session.commit()
        return new_event

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Delete person from event')
    @namespace.marshal_with(unparticipation_model)
    def delete(self):
        input_data = request.get_json()
        event = EventModel.query.filter_by(id=input_data['event_id']).first()
        event.participation.insert(input_data['person_id'])
        db.session.commit()
        return event


@namespace.route('/<int:event_id>')
class Event(Resource):
    @namespace.response(404, 'Event not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Find event by ID')
    @namespace.marshal_with(event_model)
    def get(self, event_id):
        event = EventModel.query.filter_by(id=event_id).first()
        return event

    @namespace.response(404, 'Event not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Add person to event')
    @namespace.expect(participation_model, validate=True)
    @namespace.marshal_with(participation_model)
    def post(self, event_id):
        input_data = request.get_json()
        event = EventModel.query.filter_by(id=event_id).first()
        person = PersonModel.query.filter_by(id=input_data['person_id'])
        event.participation.append(person)
        db.session.commit()
        return event

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Update event data')
    @namespace.expect(event_model, validate=True)
    @namespace.marshal_with(event_model)
    def put(self, event_id):
        input_data = request.get_json()
        event = EventModel.query.filter_by(id=event_id).first()
        event.creator=input_data['creator_id']
        event.place=input_data['place']
        event.time=input_data['time']
        event.max_player=input_data['max_player']
        event.comment=input_data['comment']
        db.session.commit()
        return event

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.doc('Delete event')
    @namespace.marshal_with(event_model)
    def delete(self, event_id):
        event = EventModel.query.filter_by(id=event_id).first()
        db.session.delete(event)
        db.session.commit()
        return event
