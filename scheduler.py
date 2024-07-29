import json
import random

from bookingrules import filter_people_who_are_booked_this_schedule, filter_people_who_were_booked_last_schedule
from filter_people_who_are_not_available import filter_people_who_are_not_available
from generate_dates import generate_dates
from print_schedule import print_schedule
from save_csv import save_csv

# load the task list
with open('tasklist.json') as f:
    task_list = json.load(f)

# load the days to schedule
with open('days.json') as f:
    days = json.load(f)

# load unavailability dates
with open('unavailability.json') as f:
    unavailable_dates = json.load(f)

def generate_schedule(task_list,  dates, n=1):
    """
    Generates a random schedule with the given task list, rules, and dates
    """
    schedules = [{"date": date, "tasks": []} for date in dates]

    for i in range(len(dates)):

        for task in task_list:
            # Get a list of the people that can do the task
            people = task['assigned'][:]  # Make a copy of the list

            people = filter_people_who_are_not_available(people, unavailable_dates, dates[i])
            # Get people who aren't already booked for this schedule
            people = filter_people_who_are_booked_this_schedule(people, schedules, i)
            # Get people that are not booked last schedule
            people= filter_people_who_were_booked_last_schedule(people, schedules, i)

            # Choose a person from the list
            if people:
                person = random.choice(people)
                schedules[i]['tasks'].append({
                    "role": task['role'],
                    "assigned": [person]
                })
                # Remove the person from the list of people who can do this task
                people.remove(person)

    return schedules

# execute the code
dates = generate_dates(days, 8)
schedule = generate_schedule(task_list,  dates)
print_schedule(schedule)
save_csv(schedule)


