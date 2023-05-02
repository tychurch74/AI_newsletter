import datetime
from datetime import datetime, timedelta


def get_seven_days_ago_date():
    today = datetime.today()
    seven_days_ago = today - timedelta(days=7)
    return seven_days_ago


def is_today_monday():
    today = datetime.today()
    return today.weekday() == 0


def convert_todays_date():
    date_string = datetime.today().strftime("%Y-%m-%d")
    date = datetime.strptime(date_string, "%Y-%m-%d")
    month = date.strftime("%B")
    day = date.strftime("%d").lstrip("0")
    year = date.strftime("%Y")

    if int(day) in [1, 21, 31]:
        day += "st"
    elif int(day) in [2, 22]:
        day += "nd"
    elif int(day) in [3, 23]:
        day += "rd"
    else:
        day += "th"

    return f"{month} {day}, {year}"






