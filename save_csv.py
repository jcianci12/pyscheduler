from convert_to_friendly_date import convert_to_friendly_date


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