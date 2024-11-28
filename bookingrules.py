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
    previousevent = None
    for index, item in enumerate(events):
        if item['id'] == event['id']:
            if index > 0:  # Check if index is greater than 0
                previousevent = events[index - 1]
                people_booked_last_schedule = [person['person_id'] for 
                                               person in previousevent['assignments'] 
                                               if 'person_id' in person
                                               ]
                
                filtered_people = [person for person in people if person['id'] not in people_booked_last_schedule]
                people = filtered_people
                return people

            else:
                return people



