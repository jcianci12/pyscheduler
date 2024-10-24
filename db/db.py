import contextlib
import sqlite3

class SchedulerDB:
    def __init__(self, db_name):
        self.db_name = db_name

    @contextlib.contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        try:
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
                CREATE TABLE IF NOT EXISTS Schedule (
                    id INTEGER PRIMARY KEY,
                    personid INTEGER,
                    taskid INTEGER,
                    eventid INTEGER,
                    FOREIGN KEY (personid) REFERENCES Person(id),
                    FOREIGN KEY (taskid) REFERENCES Task(id),
                    FOREIGN KEY (eventid) REFERENCES Event(id)
                )
            ''')

    def get_people(self, conn):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT first_name, last_name
                FROM people
            ''')
            return cur.fetchall()
    
    def create_person(self, conn, first_name, last_name):
        """Create a new person in the people table
        
        Args:
            first_name (str): The first name of the person.
            last_name (str): The last name of the person.
        
        Returns:
            int: The ID of the newly created person.
        """
        with conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO people (first_name, last_name)
                VALUES (?, ?)
            ''', (first_name, last_name))
            conn.commit()
            return cur.lastrowid

    def read_person(self, conn, person_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM people
                WHERE id = ?
            ''', (person_id,))
            return cur.fetchone()

    def update_person(self, conn, person_id, first_name, last_name):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE people
                SET first_name = ?, last_name = ?
                WHERE id = ?
            ''', (first_name, last_name, person_id))
            conn.commit()

    def delete_person(self, conn, person_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM people
                WHERE id = ?
            ''', (person_id,))
            conn.commit()

    
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

    def update_event(self, conn, event_id, event_name, event_date):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                UPDATE Event
                SET event_name = ?, event_date = ?
                WHERE id = ?
            ''', (event_name, event_date, event_id))
            conn.commit()

    def delete_event(self, conn, event_id):
        with conn:
            cur = conn.cursor()
            cur.execute('''
                DELETE FROM Event
                WHERE id = ?
            ''', (event_id,))
            conn.commit()



