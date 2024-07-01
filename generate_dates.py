import datetime


def generate_dates(days, weeks):
    """
    Generates an array of dates based on the given days and number of weeks
    """
    dates = []
    for i in range(weeks * 7):
        date = datetime.date.today() + datetime.timedelta(days=i)
        if date.strftime("%A") in days:
            dates.append(date)
    return dates