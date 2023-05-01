import datetime


def get_seven_days_ago_date():
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    return seven_days_ago


def is_today_monday():
    today = datetime.date.today()
    return today.weekday() == 0





