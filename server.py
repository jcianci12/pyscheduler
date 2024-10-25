import json

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from flask_restful import Api, Resource

from db.db import SchedulerDB

app = Flask(__name__)

Swagger(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@cross_origin()
@app.route('/people', methods=['GET'])
def get_people():
    """Get all people
    ---
    definitions:
        Person:
            type: object
            properties:
                id:
                    type: integer
                first_name:
                    type: string
                last_name:
                    type: string
    responses:
        200:
            description: A list of all people
            schema:
                type: array
                items:
                    $ref: '#/definitions/Person'
    """

    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        people = scheduler_db.get_people(conn)
    return jsonify([{'id': person[2], 'first_name': person[0], 'last_name': person[1]} for person in people])
@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    """Get a person by ID
    ---
    parameters:
        - name: person_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        200:
            description: The person
            schema:
                $ref: '#/definitions/Person'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        person = scheduler_db.read_person(conn, person_id)
        if person:
            return jsonify({'first_name': person[0], 'last_name': person[1]})
        else:
            return jsonify({'error': 'Person not found'}), 404
@cross_origin()
@app.route('/people', methods=['POST'])
def create_person():
    """Create a new person
    ---
    parameters:
        - name: person
          in: body
          schema:
            type: object
            properties:
                first_name:
                    type: string
                last_name:
                    type: string
    responses:
        201:
            description: The created person
            schema:
                $ref: '#/definitions/Person'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        person_id = scheduler_db.create_person(conn, data['first_name'], data['last_name'])
        return jsonify({'first_name': data['first_name'], 'last_name': data['last_name'], 'id': person_id}), 201


@cross_origin()
@app.route('/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    """Update a person
    ---
    parameters:
        - name: person_id
          in: path
          schema:
            type: integer
          required: true
        - name: person
          in: body
          schema:
            type: object
            properties:
                first_name:
                    type: string
                last_name:
                    type: string
    responses:
        200:
            description: The updated person
            schema:
                $ref: '#/definitions/Person'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.update_person(conn, person_id, data['first_name'], data['last_name'])
        return jsonify({'first_name': data['first_name'], 'last_name': data['last_name'], 'id': person_id})


@cross_origin()
@app.route('/people/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """Delete a person
    ---
    parameters:
        - name: person_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        204:
            description: Person deleted
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.delete_person(conn, person_id)
        return '', 204

@cross_origin()
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks
    ---
    definitions:
        Task:
            type: object
            properties:
                id:
                    type: integer
                task_name:
                    type: string
    responses:
        200:
            description: A list of all tasks
            schema:
                type: array
                items:
                    $ref: '#/definitions/Task'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        tasks = scheduler_db.get_tasks(conn)
    return jsonify([{'id': task[0], 'task_name': task[1]} for task in tasks])


@cross_origin()
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a task by ID
    ---
    parameters:
        - name: task_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        200:
            description: The task
            schema:
                $ref: '#/definitions/Task'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        task = scheduler_db.read_task(conn, task_id)
        if task:
            return jsonify({'task_name': task[0], 'id': task[2]})
        else:
            return jsonify({'error': 'Task not found'}), 404


@cross_origin()
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task
    ---
    parameters:
        - name: task_id
          in: path
          schema:
            type: integer
          required: true
        - name: task
          in: body
          schema:
            type: object
            properties:
                task_name:
                    type: string
    responses:
        200:
            description: The updated task
            schema:
                $ref: '#/definitions/Task'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.update_task(conn, task_id, data['task_name'])
        return jsonify({'task_name': data['task_name'], 'id': task_id})


@cross_origin()
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task
    ---
    parameters:
        - name: task_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        204:
            description: Task deleted
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.delete_task(conn, task_id)
        return '', 204
@cross_origin()
@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task
    ---
    parameters:
        - name: task
          in: body
          schema:
            type: object
            properties:
                task_name:
                    type: string
    responses:
        201:
            description: The created task
            schema:
                $ref: '#/definitions/Task'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        task_id = scheduler_db.create_task(conn, data['task_name'])
        return jsonify({'task_name': data['task_name'], 'id': task_id}), 201

@cross_origin()
@app.route('/events', methods=['GET'])
def get_events():
    """Get all events
    ---
    definitions:
        Event:
            type: object
            properties:
                id:
                    type: integer
                event_name:
                    type: string
                event_date:
                    type: string
    responses:
        200:
            description: A list of all events
            schema:
                type: array
                items:
                    $ref: '#/definitions/Event'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        events = scheduler_db.get_events(conn)
    return jsonify([{'id': event[0], 'event_name': event[1], 'event_date': event[2]} for event in events])

@cross_origin()
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get a single event
    ---
    parameters:
        - name: event_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        200:
            description: The event
            schema:
                $ref: '#/definitions/Event'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        event = scheduler_db.read_event(conn, event_id)
        if event:
            return jsonify({'event_name': event[1], 'event_date': event[2], 'id': event[0]})
        else:
            return jsonify({'error': 'Event not found'}), 404

@cross_origin()
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an event
    ---
    parameters:
        - name: event_id
          in: path
          schema:
            type: integer
          required: true
        - name: event
          in: body
          schema:
            type: object
            properties:
                event_name:
                    type: string
                event_date:
                    type: string
    responses:
        200:
            description: The updated event
            schema:
                $ref: '#/definitions/Event'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.update_event(conn, event_id, data['event_name'], data['event_date'])
        return jsonify({'event_name': data['event_name'], 'event_date': data['event_date'], 'id': event_id})

@cross_origin()
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event
    ---
    parameters:
        - name: event_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        204:
            description: Event deleted
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.delete_event(conn, event_id)
        return '', 204

@cross_origin()
@app.route('/events', methods=['POST'])
def create_event():
    """Create a new event
    ---
    parameters:
        - name: event
          in: body
          schema:
            type: object
            properties:
                event_name:
                    type: string
                event_date:
                    type: string
    responses:
        201:
            description: The created event
            schema:
                $ref: '#/definitions/Event'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        event_id = scheduler_db.create_event(conn, data['event_name'], data['event_date'])
        return jsonify({'event_name': data['event_name'], 'event_date': data['event_date'], 'id': event_id}), 201


if __name__ == '__main__':
    app.run(debug=True)

