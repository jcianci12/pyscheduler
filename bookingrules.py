def filter_people_who_are_booked_this_schedule(people, event):
    """
   if a person is already in the schedule, remove them
    """
    assignment_ids = [assignment.get('person_id') for assignment in event['assignments'] if 'person_id' in assignment]
    newpeople = [person for person in people if person['id'] not in assignment_ids]
    return newpeople


def remove_people_who_were_booked_last_schedule(people, event, events):
    """
    Return people who are not booked in the previous schedule
    """
    for index, item in enumerate(events):
        if item['id'] == event['id']:
            previousevent = events[index - 1]
            if previousevent is not None:
                people_booked_last_schedule = [person['person_id'] for person in previousevent['assignments'] if 'person_id' in person]
                filtered_people = [person for person in people if person['id'] not in people_booked_last_schedule]
                return filtered_people
            else:
                return people



