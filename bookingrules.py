def filter_people_who_are_booked_this_schedule(people, event):
    """
   if a person is already in the schedule, remove them
    """
    people_copy = people.copy()  # Create a copy of the original people list
    original_people_count = len(people_copy)

    #get list of people id that are in this event
    for person in event['assignments']:
        if person in people_copy:
            people_copy.remove(person)
   

    removed_people = original_people_count - len(people_copy)
    print(f"Removed {removed_people} people from the list")

    return people_copy

def remove_people_who_were_booked_last_schedule(people, lastevent):
    """
    Return people who are not booked in the previous schedule
    """
    people_copy = people.copy()  # Create a copy of the original people list
    if lastevent['assignments'] == []:
        return people
    else:
        for person in lastevent['assignments']:
            if person in people_copy:
                people_copy.remove(person)

    return people_copy



