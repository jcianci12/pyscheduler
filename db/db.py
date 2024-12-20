import contextlib
import sqlite3

class SchedulerDB:
    def __init__(self, db_name):
        self.db_name = db_name

    @contextlib.contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        try:
            self.create_table(conn)
            yield conn
        finally:
            conn.close()

    def create_table(self, conn):
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Task (
                    id INTEGER PRIMARY KEY,
                    task_name TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Event (
                    id INTEGER PRIMARY KEY,
                    event_name TEXT NOT NULL,
                    event_date DATE
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS Assignments (
                    id INTEGER PRIMARY KEY,
                    personid INTEGER,
                    taskid INTEGER,
                    eventid INTEGER,
                    FOREIGN KEY (personid) REFERENCES Person(id),
                    FOREIGN KEY (taskid) REFERENCES Task(id),
                    FOREIGN KEY (eventid) REFERENCES Event(id),
                    UNIQUE (personid, taskid, eventid)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS PersonTask (
                    person_id INTEGER NOT NULL,
                    task_id INTEGER NOT NULL,
                    PRIMARY KEY (person_id, task_id),
                    FOREIGN KEY (person_id) REFERENCES Person (id),
                    FOREIGN KEY (task_id) REFERENCES Task(id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS PersonUnavailability (
                    id INTEGER PRIMARY KEY,
                    person_id INTEGER NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    FOREIGN KEY (person_id) REFERENCES Person (id)
                )
            ''')


    def get_people(self, conn):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT first_name, last_name, id
                FROM people
                ORDER BY last_name
            ''')
            people = cur.fetchall()
            people_tasks = []
            for person in people:
                cur.execute('''
                    SELECT Task.id, Task.task_name
                    FROM PersonTask
                    INNER JOIN Task ON PersonTask.task_id = Task.id
                    WHERE PersonTask.person_id = ?
                ''', (person[2],))
                tasks = cur.fetchall()
                people_tasks.append({'first_name': person[0], 'last_name': person[1], 'id': person[2], 'tasks': [{'id': task[0], 'task_name': task[1]} for task in tasks] if tasks else []})
            return people_tasks
    
    def create_person(self, conn, data):
        """Create a new person in the people table
        
        Args:
            data (dict): A dictionary containing the first name, last name and tasks of the person.
        
        Returns:
            int: The ID of the newly created person.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO people (first_name, last_name)
                VALUES (?, ?)
            ''', (data['first_name'], data['last_name']))
            person_id = cur.lastrowid
            for task in data.get('tasks', []):
                cur.execute('''
                    INSERT INTO PersonTask (person_id, task_id)
                    VALUES (?, ?)
                ''', (person_id, task['id']))
            conn.commit()
            return person_id

    def read_person(self, conn, person_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM people
                WHERE id = ?
            ''', (person_id,))
            person = cur.fetchone()
            if person:
                cur.execute('''
                    SELECT task_name
                    FROM Task
                    INNER JOIN PersonTask ON Task.id = PersonTask.task_id
                    WHERE PersonTask.person_id = ?
                ''', (person_id,))
                tasks = cur.fetchall()
                return person, [task[0] for task in tasks]
            return None

    def update_person(self, conn, person_id, first_name, last_name, tasks):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE people
                SET first_name = ?, last_name = ?
                WHERE id = ?
            ''', (first_name, last_name, person_id))
            cur.execute('''
                DELETE FROM PersonTask
                WHERE person_id = ?
            ''', (person_id,))
            for task in tasks:
                cur.execute('''
                    INSERT INTO PersonTask (person_id, task_id)
                    VALUES (?, ?)
                ''', (person_id, task['id']))
            conn.commit()

    def delete_person(self, conn, person_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM people
                WHERE id = ?
            ''', (person_id,))
            conn.commit()
    
    def get_all_unavailability(self, conn):
        """Get all unavailability
        
        Returns:
            list: A list of tuples where each tuple contains a unavailability's id, person's id, start date, and end date.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, person_id, start_date, end_date
                FROM PersonUnavailability
            ''')
            return cur.fetchall()
    
    def create_unavailability(self, conn, person_id, start_date, end_date):
        """Create unavailability
        
        Args:
            person_id (int): The person's id.
            start_date (datetime.datetime): The start date of the unavailability.
            end_date (datetime.datetime): The end date of the unavailability.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO PersonUnavailability (person_id, start_date, end_date)
                VALUES (?, ?, ?)
            ''', (person_id, start_date, end_date))
            conn.commit()
    
    def update_unavailability(self, conn, unavailability_id, person_id, start_date, end_date):
        """Update unavailability
        
        Args:
            unavailability_id (int): The unavailability's id.
            person_id (int): The person's id.
            start_date (datetime.datetime): The start date of the unavailability.
            end_date (datetime.datetime): The end date of the unavailability.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE PersonUnavailability
                SET person_id = ?, start_date = ?, end_date = ?
                WHERE id = ?
            ''', (person_id, start_date, end_date, unavailability_id))
            conn.commit()
    
    def delete_unavailability(self, conn, person_id):
        """Delete unavailability
        
        Args:
            person_id (int): The person's id.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM PersonUnavailability
                WHERE person_id = ?
            ''', (person_id,))
            conn.commit()
    def get_tasks(self, conn):
        """Get all tasks
        
        Returns:
            list: A list of tuples where each tuple contains a task's id and name.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, task_name
                FROM Task
            ''')
            return cur.fetchall()
    
    def create_task(self, conn, task_name):
        """Create a new task in the task table
        
        Args:
            task_name (str): The name of the task.
        
        Returns:
            int: The ID of the newly created task.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO Task (task_name)
                VALUES (?)
            ''', (task_name,))
            conn.commit()
            return cur.lastrowid

    def read_task(self, conn, task_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM Task
                WHERE id = ?
            ''', (task_id,))
            return cur.fetchone()

    def update_task(self, conn, task_id, task_name):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE Task
                SET task_name = ?
                WHERE id = ?
            ''', (task_name, task_id))
            conn.commit()

    def delete_task(self, conn, task_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM Task
                WHERE id = ?
            ''', (task_id,))
            conn.commit()
    def get_events_with_assignments(self, conn):
        """Get all events with their assignments
        
        Returns:
            list: A list of tuples where each tuple contains an event's id, name, date, and a list of assignments.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT e.id, e.event_name, e.event_date, a.id AS assignment_id, a.personid, a.taskid
                FROM Event e
                LEFT JOIN Assignments a ON e.id = a.eventid
                        order by e.event_date
            ''')
            events = {}
            for row in cur.fetchall():
                event_id, event_name, event_date, assignment_id, personid, taskid = row
                if event_id not in events:
                    events[event_id] = {
                        'id': event_id,
                        'event_name': event_name,
                        'event_date': event_date,
                        'assignments': []
                    }
                if assignment_id is not None:
                    events[event_id]['assignments'].append({
                        'id': assignment_id,
                        'event_id': event_id,
                        'task_id': taskid,
                        'person_id': personid
                    })
            return list(events.values())
    def create_event(self, conn, event_name, event_date):
        """Create a new event in the event table
        
        Args:
            event_name (str): The name of the event.
            event_date (date): The date of the event.
        
        Returns:
            int: The ID of the newly created event.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO Event (event_name, event_date)
                VALUES (?, ?)
            ''', (event_name, event_date))
            conn.commit()
            return cur.lastrowid

    def read_event(self, conn, event_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM Event
                WHERE id = ?
            ''', (event_id,))
            return cur.fetchone()

    def update_event(self, conn, event_id, event_name, event_date, assignments):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE Event
                SET event_name = ?, event_date = ?
                WHERE id = ?
            ''', (event_name, event_date, event_id))
            cur.execute('''
                DELETE FROM Assignments
                WHERE eventid = ?
            ''', (event_id,))
            for assignment in assignments:
                cur.execute('''
                    INSERT INTO Assignments (eventid, taskid, personid)
                    VALUES (?, ?, ?)
                ''', (event_id, assignment['task_id'], assignment['person_id']))
            conn.commit()

    def delete_event(self, conn, event_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM Event
                WHERE id = ?
            ''', (event_id,))
            conn.commit()


    def create_assignment(self, conn, event_id, task_id, person_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT 1 FROM Assignments
                WHERE eventid = ? AND taskid = ? AND personid = ?
            ''', (event_id, task_id, person_id))
            if cur.fetchone() is None:
                cur.execute('''
                    INSERT INTO Assignments (eventid, taskid, personid)
                    VALUES (?, ?, ?)
                ''', (event_id, task_id, person_id))
                conn.commit()
                return cur.lastrowid
            else:
                raise ValueError("Assignment already exists")

    def read_assignment(self, conn, assignment_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM Assignments
                WHERE id = ?
            ''', (assignment_id,))
            return cur.fetchone()

    def update_assignment(self, conn, assignment_id, event_id, task_id, person_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE Assignments
                SET eventid = ?, taskid = ?, personid = ?
                WHERE id = ?
            ''', (event_id, task_id, person_id, assignment_id))
            conn.commit()

    def delete_assignment(self, conn, assignment_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM Assignments
                WHERE id = ?
            ''', (assignment_id,))
            conn.commit()

    def get_all_assignments(self, conn):
        """Get all assignments
        
        Returns:
            list: A list of tuples where each tuple contains an assignment's id, event id, task id, and person id.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, eventid, taskid, personid
                FROM Assignments
            ''')
            return cur.fetchall()
    
    def get_assignments_by_event_id(self, conn, id):
        """Get all assignments with event id matching the id passed in
        
        Returns:
            list: A list of tuples where each tuple contains an assignment's id, event id, task id, and person id.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, eventid, taskid, personid
                FROM Assignments
                WHERE eventid = ?
            ''', (id,))
            return cur.fetchall()
