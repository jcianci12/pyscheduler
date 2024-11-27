import datetime


def filter_people_who_are_not_available(people,unavailable_dates, date):
    """
    Remove people who are not available from the list of people. The format of the data looks like this:
    [{"name":"TH","unavailable date range":{"start":"2024-07-01","end":"2024-07-15"}}]
    """
#the schema looks like this:
#  Returns:
#             list: A list of tuples where each tuple contains a unavailability's id, person's id, start date, and end date.
       

    # people_copy = people.copy()  # Create a copy of the original people list
    # people_not_available = []

    # for person in people_copy:
    #     for unavailable_date in unavailable_dates:
    #         try:
    #             start_date = datetime.datetime.strptime(unavailable_date[2], "%Y-%m-%d").date()
    #             end_date = datetime.datetime.strptime(unavailable_date[3], "%Y-%m-%d").date()
    #             date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    #         except ValueError:
    #             print(f"Invalid date format for {unavailable_date[2]} or {unavailable_date[3]} or {date}")
    #             raise
    #         if person['id'] == unavailable_date[1] and start_date <= date_obj <= end_date:
    #             people_not_available.append(person)

    # for person in people_not_available:
    #     if person in people_copy:
    #         people_copy.remove(person)

    # return people_copy
    return people
def filter_people_who_can_do_this_task(people, assignment):
    """
    Return people who are able to do this task
    """
    if people is None:
        return []
    return [
        person
        for person in people
        if any(
            task['id'] == assignment['task_id']
            for task in person['tasks']
        )
    ]