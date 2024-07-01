import datetime


def filter_people_who_are_not_available(people, unavailable_dates, date):
    """
    Remove people who are not available from the list of people. The format of the data looks like this:
    [{"name":"TH","unavailable date range":{"start":"2024-07-01","end":"2024-07-15"}}]
    """
    people_copy = people.copy()  # Create a copy of the original people list
    people_not_available = []

    for person in people_copy:
        for unavailable_date in unavailable_dates:
            try:
                start_date = datetime.datetime.strptime(unavailable_date['unavailable date range']['start'], "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(unavailable_date['unavailable date range']['end'], "%Y-%m-%d").date()
                date_obj = date
            except ValueError:
                print(f"Invalid date format for {unavailable_date['unavailable date range']['start']} or {unavailable_date['unavailable date range']['end']} or {date}")
                raise
            if person['name'] == unavailable_date['name'] and start_date <= date_obj <= end_date:
                people_not_available.append(person)

    for person in people_not_available:
        if person in people_copy:
            people_copy.remove(person)

    return people_copy