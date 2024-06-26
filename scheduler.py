import datetime
import json
import random

from no_consecutive_tasks import no_consecutive_tasks
from no_same_task_consecutive_days import no_same_task_consecutive_schedules
from no_same_task_same_time import no_schedule_double_booking, return_people_who_are_not_booked_on_previous_schedule

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
# define the scheduling rules
scheduling_rules = [no_schedule_double_booking]


def generate_random_schedule(task_list, rules, dates, n=1):
    """
    Generates a random schedule with the given task list, rules, and dates
    """
    schedules = [{"date": date, "tasks": []} for date in dates]

    for i, schedule in enumerate(schedules):

        for task in task_list:
            # Get a list of the people that can do the task
            people = task['assigned']

            index = min(i, len(schedules) - 1)
            # peoplethatarenotalreadybookedthisschedule = no_schedule_double_booking(people, schedules, index)
            peoplethatarenotalreadybookedpreviousschedule = return_people_who_are_not_booked_on_previous_schedule(people, schedules, index)
            # names2 = set(item['name'] for item in peoplethatarenotalreadybookedpreviousschedule)
            # intersection = [item for item in peoplethatarenotalreadybookedthisschedule if item['name'] in names2]
            person = random.choice(peoplethatarenotalreadybookedpreviousschedule)


            schedule['tasks'].append({
                "role": task['role'],
                "assigned": [person]
            })

    return schedules


def print_schedule(schedule):
    # Calculate the maximum task name length
    max_task_len = max(len(task['role']) for day in schedule for task in day['tasks'])

    # Print table header
    print(f"{'Date':12} {'Task':{max_task_len}} {'Assigned':12}")
    print('-' * (20 + max_task_len + 12))

    # Print each day's tasks
    for day in schedule:
        print(f"{day['date']:12}")
        for task in day['tasks']:
            print(f"{' ' * 12}{task['role'].ljust(max_task_len)} {task['assigned'][0]['name']:12}")
        print()



# execute the code
dates = generate_dates(days, 4)
schedule = generate_random_schedule(task_list, scheduling_rules, dates)
print_schedule(schedule)


