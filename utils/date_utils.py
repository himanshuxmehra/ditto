from dateutil import parser
from datetime import datetime, timedelta
import re

def parse_relative_time(time_string):
    now = datetime.now()
    
    # Handle "now" case
    if time_string.lower() == 'now':
        return now

    # Handle "in X minutes/hours/etc." case
    match = re.match(r'in\s+(\d+)\s*(min|minute|hour|day|week|month|year)s?', time_string, re.IGNORECASE)
    if match:
        amount, unit = match.groups()
        amount = int(amount)
        unit = unit.lower()
        
        if unit.startswith('min'):
            return now + timedelta(minutes=amount)
        elif unit == 'hour':
            return now + timedelta(hours=amount)
        elif unit == 'day':
            return now + timedelta(days=amount)
        elif unit == 'week':
            return now + timedelta(weeks=amount)
        elif unit == 'month':
            return now + timedelta(days=amount*30)  # Approximate
        elif unit == 'year':
            return now + timedelta(days=amount*365)  # Approximate

    # Handle "X minutes/hours/etc. from now" case
    match = re.match(r'(\d+)\s*(min|minute|hour|day|week|month|year)s?\s+from\s+now', time_string, re.IGNORECASE)
    if match:
        amount, unit = match.groups()
        amount = int(amount)
        unit = unit.lower()
        
        if unit.startswith('min'):
            return now + timedelta(minutes=amount)
        elif unit == 'hour':
            return now + timedelta(hours=amount)
        elif unit == 'day':
            return now + timedelta(days=amount)
        elif unit == 'week':
            return now + timedelta(weeks=amount)
        elif unit == 'month':
            return now + timedelta(days=amount*30)  # Approximate
        elif unit == 'year':
            return now + timedelta(days=amount*365)  # Approximate
    
    return None

def parse_date(date_string):
    try:
        # First, try to parse as a relative time
        relative_date = parse_relative_time(date_string)
        if relative_date:
            return relative_date.strftime("%Y-%m-%d %H:%M")
        
        # If not a relative time, try to parse as an absolute date
        return parser.parse(date_string).strftime("%Y-%m-%d %H:%M")
    except parser.ParserError:
        raise ValueError(f"Unable to parse date: {date_string}")

def parse_datetime(datetime_string):
    return parse_date(datetime_string)  # We can use the same function for both