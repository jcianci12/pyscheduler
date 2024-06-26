def convert_to_friendly_date(date):
    day = date.strftime("%a")
    day_num = date.strftime("%d")
    month = date.strftime("%b")
    year = date.strftime("%Y")

    day_of_month = int(day_num)
    if day_of_month % 10 == 1 and day_of_month != 11:
        day_num += "st"
    elif day_of_month % 10 == 2 and day_of_month != 12:
        day_num += "nd"
    elif day_of_month % 10 == 3 and day_of_month != 13:
        day_num += "rd"
    else:
        day_num += "th"

    return f"{day} {day_num} of {month} {year}"