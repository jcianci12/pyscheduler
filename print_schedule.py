def print_schedule(schedule):
    """
    Prints the schedule
    """
    for schedule in schedule:
        print(f"Date: {schedule['date']}")
        for task in schedule['tasks']:
            print(f"  {task['role']}: {', '.join([person['name'] for person in task['assigned']])}")
        print()