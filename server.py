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
    with SchedulerDB('scheduler.db') as db:
        with SchedulerDB.connect(db).cursor() as cursor:
            people = SchedulerDB.get_people(cursor)
            return jsonify([{'id': person[0], 'first_name': person[1], 'last_name': person[2]} for person in people])

@app.route('/people', methods=['POST'])
def create_person():
    """Create a new person

    ---
    parameters:
        - in: body
          name: body
          description: The person to create.
          schema:
            type: object
            required:
                - first_name
                - last_name
            properties:
                first_name:
                    type: string
                last_name:
                    type: string
    responses:
        200:
            description: The created person
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    first_name:
                        type: string
                    last_name:
                        type: string
    """
    data = request.get_json()
    with SchedulerDB('scheduler.db').connect() as conn:
        person_id = SchedulerDB.create_person(conn, data['first_name'], data['last_name'])
        return jsonify({'id': person_id, 'first_name': data['first_name'], 'last_name': data['last_name']})


@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    """Get a person by ID

    ---
    parameters:
        - in: path
          name: person_id
          description: The ID of the person.
          schema:
            type: integer
    responses:
        200:
            description: The person
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    first_name:
                        type: string
                    last_name:
                        type: string
        404:
            description: Person not found
            schema:
                type: object
                properties:
                    error:
                        type: string
    """
    with SchedulerDB('scheduler.db').connect() as conn:
        person = SchedulerDB.read_person(conn, person_id)
        if person:
            return jsonify({'id': person[0], 'first_name': person[1], 'last_name': person[2]})
        else:
            return jsonify({'error': 'Person not found'}), 404


@app.route('/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    """Update a person by ID

    ---
    parameters:
        - in: path
          name: person_id
          description: The ID of the person.
          schema:
            type: integer
        - in: body
          name: body
          description: The updated person.
          schema:
            type: object
            required:
                - first_name
                - last_name
            properties:
                first_name:
                    type: string
                last_name:
                    type: string
    responses:
        200:
            description: The updated person
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    first_name:
                        type: string
                    last_name:
                        type: string
        404:
            description: Person not found
            schema:
                type: object
                properties:
                    error:
                        type: string
    """
    data = request.get_json()
    with SchedulerDB('scheduler.db').connect() as conn:
        person = SchedulerDB.update_person(conn, person_id, data['first_name'], data['last_name'])
        if person:
            return jsonify({'id': person[0], 'first_name': person[1], 'last_name': person[2]})
        else:
            return jsonify({'error': 'Person not found'}), 404


@app.route('/people/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """Delete a person by ID

    ---
    parameters:
        - in: path
          name: person_id
          description: The ID of the person.
          schema:
            type: integer
    responses:
        200:
            description: Person deleted
            schema:
                type: object
                properties:
                    message:
                        type: string
    """
    with SchedulerDB('scheduler.db').connect() as conn:
        SchedulerDB.delete_person(conn, person_id)
        return jsonify({'message': 'Person deleted'})





if __name__ == '__main__':
    app.run(debug=True)

