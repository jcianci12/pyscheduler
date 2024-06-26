def no_schedule_double_booking(people, schedules, index):
    """
    Remove people on the schedule from the list of people
    """
    people_copy = people.copy()  # Create a copy of the original people list
    original_people_count = len(people_copy)
    
    for task in schedules[index]['tasks']:
        for person in task['assigned']:
            if person in people_copy:
                people_copy.remove(person)

    removed_people = original_people_count - len(people_copy)
    print(f"Removed {removed_people} people from the list, index {index}")

    return people_copy

def return_people_who_are_not_booked_on_previous_schedule(people, schedules, index):
    """
    Return people who are not booked in the previous schedule
    """
    people_copy = people.copy()  # Create a copy of the original people list
    peopleonpreviousschedule = return_list_of_people_who_are_booked_on_previous_schedule(people, schedules, index)
    intersection = []
    for person in people_copy:
        if person not in peopleonpreviousschedule:
            intersection.append(person)

    # print(f"Removed {len(people_copy)-len(intersection)} people from the list, index {index}")
    # print(intersection)
    return intersection

def return_list_of_people_who_are_booked_on_previous_schedule(people, schedules, index):
    """
    Return list of people who are booked in the previous schedule under any task
    """
    people_copy = []  # Create a copy of the original people list
    #loop through the list of tasks in the previous schedule
    for task in schedules[index-1]['tasks']:
        for person in task['assigned']:
            people_copy.append(person)

    # print(people_copy)
    return people_copy
