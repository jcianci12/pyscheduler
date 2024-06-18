import json
import random

# load the task list
with open('tasklist.json') as f:
    task_list = json.load(f)

# load the days to schedule
with open('days.json') as f:
    days = json.load(f)

# define a scheduling rule
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
def no_consecutive_tasks(person, schedule):
    """
    Checks if a person is on two consecutive tasks
    """
    for day in schedule:
        for i in range(len(day['tasks'])-1):
            if day['tasks'][i]['assigned'][0]['name'] == person and \
               day['tasks'][i+1]['assigned'][0]['name'] == person:
                return False
    return True

# define a scheduling rule
def no_same_task_consecutive_days(person, schedule):
    """
    Checks if a person is on the same task on consecutive days
    """
    for i in range(len(schedule)-1):
        if schedule[i]['tasks'][0]['assigned'][0]['name'] == person and \
           schedule[i+1]['tasks'][0]['assigned'][0]['name'] == person and \
           schedule[i]['tasks'][0]['name'] == schedule[i+1]['tasks'][0]['name']:
            return False
    return True

# define the scheduling rules
scheduling_rules = [no_same_task_same_time, no_consecutive_tasks, no_same_task_consecutive_days]

def check_schedule(schedule, rules):
    """
    Checks if a schedule meets all the scheduling rules
    """
    for day in schedule:
        if day['date'] not in days:
            return False
        for task in day['tasks']:
            person = task['assigned'][0]['name']
            if not all(rule(person, schedule) for rule in rules):
                return False
    return True


# generate a random schedule
def generate_random_schedule(task_list, rules, dates):
    """
    Generates a random schedule that meets all the scheduling rules
    """
    schedules = []
    for _ in range(4):
        schedule = []
        for day in dates:
            tasks = []
            assigned_people = []
            for task in task_list[dates.index(day)]['name']:
                while True:
                    person = random.choice(task['assigned'])
                    if person['name'] not in assigned_people:
                        assigned_people.append(person['name'])
                        break
                task['assigned'] = [person]
                while not all(rule(person['name'], schedule) for rule in rules):
                    person = random.choice(task['assigned'])
                    task['assigned'] = [person]
                tasks.append(task)
            schedule.append({'date': day, 'tasks': tasks})
        schedules.append(schedule)
    # remove schedules that don't meet all rules
    schedules = [schedule for schedule in schedules if check_schedule(schedule, scheduling_rules)]

    # print the schedules
    for schedule in schedules:
        for day in schedule:
            print(day['date'])
            for task in day['tasks']:
                print(task['name'] + ': ' + task['assigned'][0]['name'])
        print('')

# execute the code
dates = [f'2019-01-{i+1}' for i in range(7, 28)]
generate_random_schedule(task_list, scheduling_rules, dates)


