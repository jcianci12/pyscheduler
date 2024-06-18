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