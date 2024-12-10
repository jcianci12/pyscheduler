
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flasgger import Swagger

from db.db import SchedulerDB
from scheduler import allocate_tasks_for_event
from flask import Flask, jsonify, url_for
from flask_httpauth import HTTPTokenAuth
import requests
import jwt


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '7hY48mDD1MCqW6irlkdvY61Vq1DiOPIVKCcpPxkAKn3un2JXyY6N2Knm0SHGOA2uzdo7zJQpz1ax3R6kxH6NWQyHJz6rKXodBJ2lqk9sQk6Y6pjaPkH1xFpoKrC3SeMd'


Swagger(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



auth = HTTPTokenAuth(scheme='Bearer')



auth = HTTPTokenAuth(scheme='Bearer')

def fetch_jwk():
    api_endpoint = "https://authentik.tekonline.com.au/application/o/pyscheduler/jwks/"
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch JWK")
        return None

@auth.verify_token
def verify_token(token):
    try:
        print(request.headers)
        jwk = fetch_jwk()
        if jwk is None:
            return False
        # Extract the public key
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk['keys'][0])
    except Exception as e:
        print("Error fetching or parsing JWK:", str(e))
        return str(e)
    
    try:
        # Decode the JWT
        data = jwt.decode(token, public_key, algorithms=['RS256'], audience="yJwnySrODx2x1uNDKzszWiTV3ivrLPBdvvDkz1sN")
        print("Token decoded successfully:", data)
        return data  # Return the username as a string
    except Exception as e:
        print("Error decoding token:", str(e))
        return str(e)

@app.route('/xyz', methods=['GET'])
@auth.login_required
def xyz():
    """Test the authentication
    ---
    responses:
        200:
            description: Hello message
            schema:
                type: object
                properties:
                    acr:
                        type: string
                    amr:
                        type: array
                        items:
                            type: string
                    aud:
                        type: string
                    auth_time:
                        type: integer
                    azp:
                        type: string
                    email:
                        type: string
                    email_verified:
                        type: boolean
                    exp:
                        type: integer
                    given_name:
                        type: string
                    groups:
                        type: array
                        items:
                            type: string
                    iat:
                        type: integer
                    iss:
                        type: string
                    name:
                        type: string
                    nickname:
                        type: string
                    nonce:
                        type: string
                    preferred_username:
                        type: string
                    sub:
                        type: string
                    uid:
                        type: string
    """
    
    return  jsonify(auth.current_user())

def get_logged_in_user_or_demo_db():
    if auth.current_user():
        return auth.current_user()
    else:
        return 'scheduler.db'

@cross_origin()
@app.route('/getpeople', methods=['GET'])
def getpeople():
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
                tasks:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                            task_name:
                                type: string
    responses:
        200:
            description: A list of all people
            schema:
                type: array
                items:
                    $ref: '#/definitions/Person'
    """

    scheduler_db = SchedulerDB(get_logged_in_user_or_demo_db())
    with scheduler_db.connect() as conn:
        people = scheduler_db.get_people(conn)
    return jsonify(people)




@app.route('/getperson/<int:person_id>', methods=['GET'])
def getperson(person_id):
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
@app.route('/createperson', methods=['POST'])
def createperson():
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
                tasks:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
    responses:
        201:
            description: The created person
            schema:
                $ref: '#/definitions/Person'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        person_id = scheduler_db.create_person(conn, data)
        return jsonify({'first_name': data['first_name'], 'last_name': data['last_name'], 'id': person_id}), 201

@cross_origin()
@app.route('/updateperson/<int:person_id>', methods=['PUT'])
def updateperson(person_id):
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
                tasks:
                    type: array
                    items:
                        type: integer
    responses:
        200:
            description: The updated person
            schema:
                $ref: '#/definitions/Person'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.update_person(conn, person_id, data['first_name'], data['last_name'], data.get('tasks', []))
        return jsonify({'first_name': data['first_name'], 'last_name': data['last_name'], 'id': person_id})


@cross_origin()
@app.route('/deleteperson/<int:person_id>', methods=['DELETE'])
def deleteperson(person_id):
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
@app.route('/unavailability', methods=['GET'])
def get_unavailability():
    """Get all unavailability
    ---
    definitions:
        Unavailability:
            type: object
            properties:
                id:
                    type: integer
                person_id:
                    type: integer
                start_date:
                    type: string
                end_date:
                    type: string
    responses:
        200:
            description: A list of all unavailability
            schema:
                type: array
                items:
                    $ref: '#/definitions/Unavailability'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        unavailability = scheduler_db.get_all_unavailability(conn)
        return jsonify([{'id': unavail[0], 'person_id': unavail[1], 'start_date': unavail[2], 'end_date': unavail[3]} for unavail in unavailability])
@cross_origin()
@app.route('/unavailability', methods=['POST'])
def create_unavailability():
    """Create new unavailability
    ---
    parameters:
        - name: unavailability
          in: body
          schema:
            type: object
            properties:
                person_id:
                    type: integer
                start_date:
                    type: string
                    format: date
                end_date:
                    type: string
                    format: date
    responses:
        201:
            description: The created unavailability
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    person_id:
                        type: integer
                    start_date:
                        type: string
                    end_date:
                        type: string
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        unavailability_id = scheduler_db.create_unavailability(conn, data['person_id'], data['start_date'], data['end_date'])
        return jsonify({'id': unavailability_id, 'person_id': data['person_id'], 'start_date': data['start_date'], 'end_date': data['end_date']}), 201
@cross_origin()
@app.route('/unavailability/<int:unavailability_id>', methods=['PUT'])
def update_unavailability(unavailability_id):
    """Update an unavailability
    ---
    parameters:
        - name: unavailability_id
          in: path
          schema:
            type: integer
          required: true
        - name: unavailability
          in: body
          schema:
            type: object
            properties:
                person_id:
                    type: integer
                start_date:
                    type: string
                    format: date

                end_date:
                    type: string
                    format: date

    responses:
        201:
            description: The updated unavailability
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    person_id:
                        type: integer
                    start_date:
                        type: string
                        format: date
                    end_date:
                        type: string
                        format: date
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.update_unavailability(conn, unavailability_id, data['person_id'], data['start_date'], data['end_date'])
        return jsonify({'id': unavailability_id, 'person_id': data['person_id'], 'start_date': data['start_date'], 'end_date': data['end_date']}), 201
    # def create_unavailability(self, conn, person_id, start_date, end_date):


@cross_origin()
@app.route('/unavailability/<int:unavailability_id>', methods=['DELETE'])
def delete_unavailability(unavailability_id):
    """Delete an unavailability
    ---
    parameters:
        - name: unavailability_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        204:
            description: Unavailability deleted
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.delete_unavailability(conn, unavailability_id)
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
            return jsonify({'task_name': task[0], 'id': task[1]})
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
        events = scheduler_db.get_events_with_assignments(conn)
    return jsonify(events)


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
                assignments:
                    type: array
                    items:
                        $ref: '#/definitions/Assignment'
    responses:
        200:
            description: The updated event
            schema:
                $ref: '#/definitions/Event'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.update_event(conn, event_id, data['event_name'], data['event_date'], data['assignments'])
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


@cross_origin()
@app.route('/allocate', methods=['POST'])
def allocate():
    """Allocate tasks for an event
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
        200:
            description: The updated event
            schema:
                $ref: '#/definitions/Event'
    """
    event = request.get_json()
    event = allocate_tasks_for_event(event)
    return jsonify(event)
    

@cross_origin()
@app.route('/assignments', methods=['GET'])
def get_all_assignments():
    """Get all assignments
    ---
    definitions:
        Assignment:
            type: object
            properties:
                id:
                    type: integer
                event_id:
                    type: integer
                task_id:
                    type: integer
                person_id:
                    type: integer
    responses:
        200:
            description: A list of all assignments
            schema:
                type: array
                items:
                    $ref: '#/definitions/Assignment'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        assignments = scheduler_db.get_all_assignments(conn)
    return jsonify([{'id': assignment[0], 'event_id': assignment[1], 'task_id': assignment[2], 'person_id': assignment[3]} for assignment in assignments])
@cross_origin()
@app.route('/eventswithassignments', methods=['GET'])
def get_events_with_assignments():
    """Get all events with their assignments
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
                assignments:
                    type: array
                    items:
                        $ref: '#/definitions/Assignment'
        Assignment:
            type: object
            properties:
                id:
                    type: integer
                event_id:
                    type: integer
                task_id:
                    type: integer
                person_id:
                    type: integer
    responses:
        200:
            description: A list of all events with their assignments
            schema:
                type: array
                items:
                    $ref: '#/definitions/Event'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        events = scheduler_db.get_events_with_assignments(conn)
    return jsonify(events)
@cross_origin()
@app.route('/assignments/<int:assignment_id>', methods=['GET'])
def get_assignment(assignment_id):
    """Get an assignment
    ---
    definitions:
        Assignment:
            type: object
            properties:
                id:
                    type: integer
                event_id:
                    type: integer
                task_id:
                    type: integer
                person_id:
                    type: integer
    parameters:
        - name: assignment_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        200:
            description: The assignment
            schema:
                $ref: '#/definitions/Assignment'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        assignment = scheduler_db.read_assignment(conn, assignment_id)
    return jsonify({'id': assignment[0], 'event_id': assignment[1], 'task_id': assignment[2], 'person_id': assignment[3]})
@cross_origin()
@app.route('/test123/<int:event_id>', methods=['GET'])
def test123(event_id):
    """Get all assignments by event ID
    ---
    parameters:
        - name: event_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        200:
            description: A list of assignments for the specified event
            schema:
                type: array
                items:
                    $ref: '#/definitions/Assignment'
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        assignments = scheduler_db.get_assignments_by_event_id(conn, event_id)
    return jsonify([{'id': assignment[0], 'event_id': assignment[1], 'task_id': assignment[2], 'person_id': assignment[3]} for assignment in assignments])

@cross_origin()
@app.route('/assignments', methods=['POST'])
def create_assignment():
    """Create a new assignment
    ---
    parameters:
        - name: assignment
          in: body
          schema:
            type: object
            properties:
                event_id:
                    type: integer
                task_id:
                    type: integer
                person_id:
                    type: integer
    responses:
        201:
            description: The created assignment
            schema:
                $ref: '#/definitions/Assignment'
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        assignment_id = scheduler_db.create_assignment(conn, data['event_id'], data['task_id'], data['person_id'])
        return jsonify({'id': assignment_id, 'event_id': data['event_id'], 'task_id': data['task_id'], 'person_id': data['person_id']}), 201
@cross_origin()
@app.route('/assignments/<int:assignment_id>', methods=['PUT'])
def update_assignment(assignment_id):
    """Update an assignment
    ---
    parameters:
        - name: assignment_id
          in: path
          schema:
            type: integer
          required: true
        - name: assignment
          in: body
          schema:
            type: object
            properties:
                event_id:
                    type: integer
                task_id:
                    type: integer
                person_id:
                    type: integer
    responses:
        204:
            description: Assignment updated
    """
    data = request.get_json()
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.update_assignment(conn, assignment_id, data['event_id'], data['task_id'], data['person_id'])
        return '', 204

@cross_origin()
@app.route('/assignments/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    """Delete an assignment
    ---
    parameters:
        - name: assignment_id
          in: path
          schema:
            type: integer
          required: true
    responses:
        204:
            description: Assignment deleted
    """
    scheduler_db = SchedulerDB('scheduler.db')
    with scheduler_db.connect() as conn:
        scheduler_db.delete_assignment(conn, assignment_id)
        return '', 204




if __name__ == '__main__':
    app.run(debug=False)


