
from datetime import datetime


def convert_to_human_readable(day, month):
    date_obj = datetime.strptime(f'{month}-{day}', '%m-%d')
    human_readable_date = date_obj.strftime('%B %d')

    return human_readable_date
