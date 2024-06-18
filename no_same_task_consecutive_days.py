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