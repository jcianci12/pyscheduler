import datetime
import json
import random

from bookingrules import filter_people_who_are_booked_this_schedule, filter_people_who_were_booked_last_schedule

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
            dates.append(date)
    return dates
# define the scheduling rules
scheduling_rules = [filter_people_who_are_booked_this_schedule]


def generate_random_schedule(task_list, rules, dates, n=1):
    """
    Generates a random schedule with the given task list, rules, and dates
    """
    schedules = [{"date": date, "tasks": []} for date in dates]

    for i in range(len(dates)):

        for task in task_list:
            # Get a list of the people that can do the task
            people = task['assigned'][:]  # Make a copy of the list

            # Get people who aren't already booked for this schedule
            peoplethatarenotalreadybookedthisdate = filter_people_who_are_booked_this_schedule(people, schedules, i)
            peoplethatarenotbookedlastschedule= filter_people_who_were_booked_last_schedule(peoplethatarenotalreadybookedthisdate, schedules, i)

            # Choose a person from the list
            if peoplethatarenotbookedlastschedule:
                person = random.choice(peoplethatarenotbookedlastschedule)
                schedules[i]['tasks'].append({
                    "role": task['role'],
                    "assigned": [person]
                })
                # Remove the person from the list of people who can do this task
                people.remove(person)

    return schedules


def print_schedule(schedule):
    """
    Prints the schedule
    """
    for schedule in schedule:
        print(f"Date: {schedule['date']}")
        for task in schedule['tasks']:
            print(f"  {task['role']}: {', '.join([person['name'] for person in task['assigned']])}")
        print()

def save_csv(schedules):
    """
    saves a new schedule in csv format. 
put all tasks for a date on a single row.
    """
    csvobject = []
    headerrow = [""]
    for task in schedules[0]['tasks']:
        headerrow.append(task['role'])            
    csvobject.append(headerrow)
    
    for schedule in schedules:
        row = [ convert_to_friendly_date(  schedule['date'])]
        for task in schedule['tasks']:
            # row.append(task['role'])
            for person in task['assigned']:
                row.append(person['name'])
        csvobject.append(row)

    with open('schedule.csv', 'w') as f:
        for row in csvobject:
            f.write(','.join(row) + '\n')
                
def convert_to_friendly_date(date):
    day = date.strftime("%a")
    day_num = date.strftime("%d")
    month = date.strftime("%b")
    year = date.strftime("%Y")
    
    day_of_month = int(day_num)
    if day_of_month % 10 == 1 and day_of_month != 11:
        day_num += "st"
    elif day_of_month % 10 == 2 and day_of_month != 12:
        day_num += "nd"
    elif day_of_month % 10 == 3 and day_of_month != 13:
        day_num += "rd"
    else:
        day_num += "th"
    
    return f"{day} {day_num} of {month} {year}"




# execute the code
dates = generate_dates(days, 4)
schedule = generate_random_schedule(task_list, scheduling_rules, dates)
print_schedule(schedule)
save_csv(schedule)


