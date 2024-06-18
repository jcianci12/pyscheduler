import datetime
import json
import random

from no_consecutive_tasks import no_consecutive_tasks
from no_same_task_consecutive_days import no_same_task_consecutive_days

# load the task list
with open('tasklist.json') as f:
    task_list = json.load(f)

# load the days to schedule
with open('days.json') as f:
    days = json.load(f)

def generate_dates(days, weeks):
    """
    Generates an array of dates based on the given days and number of weeks
    """
    dates = []
    for i in range(weeks * 7):
        date = datetime.date.today() + datetime.timedelta(days=i)
        if date.strftime("%A") in days:
            dates.append(date.strftime("%Y-%m-%d"))
    return dates
def no_same_task_same_time(person, schedule):
    """
    Checks if a person is on the same task at the same time as another person
    """
    for day in schedule:
        for task in day['tasks']:
            if task['assigned'][0]['name'] == person:
                for other_task in day['tasks']:
                    if other_task['assigned'][0]['name'] != person and \
                       task['name'] == other_task['name']:
                        return False
    return True

# define a scheduling rule
# define a scheduling rule
# define the scheduling rules
scheduling_rules = [no_same_task_same_time, no_consecutive_tasks, no_same_task_consecutive_days]



# generate a random schedule
def generate_random_schedule(task_list, rules, dates, n=1):
    """
    Generates a random schedule with the given task list, rules, and dates
    """
    schedule = []
    for i in range(n*7):
        day = {
            "date": dates[(i + 7) % len(dates)],
            "tasks": []
        }
        for task in task_list:
            people = task['assigned']
            person = random.choice(people)
            while not all(rule(person['name'], schedule) for rule in rules):
                person = random.choice(people)
            day['tasks'].append({
                "name": task['name'],
                "assigned": [person]
            })
        schedule.append(day)
    return schedule

def print_schedule(schedule):
    for day in schedule:
        print(day['date'])
        for task in day['tasks']:
            print(f"  {task['name']}: {task['assigned'][0]['name']}")



# execute the code
dates = generate_dates(days, 4)
schedule = generate_random_schedule(task_list, scheduling_rules, dates)
print_schedule(schedule)


