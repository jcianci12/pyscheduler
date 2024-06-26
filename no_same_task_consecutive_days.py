def no_same_task_consecutive_schedules(people, schedule):
    """
    Checks if any person is on the same task on consecutive days
    """
    people_to_remove = set()
    for day in range(len(schedule)-1):
        tasks = [schedule[day]['tasks'][0]['name'], schedule[day+1]['tasks'][0]['name']]
        for person in people:
            if person in schedule[day]['tasks'][0]['assigned'][0]['name'] and \
               person in schedule[day+1]['tasks'][0]['assigned'][0]['name'] and \
               schedule[day]['tasks'][0]['name'] in tasks:
                people_to_remove.add(person)
    return [person for person in people if person not in people_to_remove]
