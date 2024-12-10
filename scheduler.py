import json
import random

from bookingrules import filter_people_who_are_booked_this_schedule, remove_people_who_were_booked_last_schedule
from filter_people_who_are_not_available import filter_people_who_are_not_available, filter_people_who_can_do_this_task
from generate_dates import generate_dates
from print_schedule import print_schedule
from save_csv import save_csv
from db.db import SchedulerDB
from typing import List, Dict



def allocate_tasks_for_event(event,dbname):
    
#load the data we need
    scheduler_db = SchedulerDB(dbname)
    with scheduler_db.connect() as conn:
        people = scheduler_db.get_people(conn)
        unavailable_dates=scheduler_db.get_all_unavailability(conn)
        days = scheduler_db.get_events_with_assignments(conn)
        events = scheduler_db.get_events_with_assignments(conn)
        #gets a list of people and the tasks they can do
        # gets the unavailable dates
        unavailable_dates=scheduler_db.get_all_unavailability(conn)
        

    #loop through the assignments in the event, and try to assign the 
# people to the tasks but only if the person is available and is allowed to do that task
        # people = filter_people_who_are_not_available(people, unavailable_dates,event['event_date'])
        # Get people who aren't already booked for this schedule
        # get the index of the current event
        



        for assignment in event['assignments']:
            people= remove_people_who_were_booked_last_schedule(people, event,events)

            people = filter_people_who_can_do_this_task(people, assignment)
            people = filter_people_who_are_booked_this_schedule(people, event)

            if people == []:
                assignment['person_id'] = None
            else:

                person = random.choice(people)
            # Assign the person to the task
                assignment['person_id'] = person['id']
                
    return event




