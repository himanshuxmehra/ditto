from database.db_operations import get_db_connection
from utils.date_utils import parse_datetime

def add_schedule(event, start_time, end_time):
    conn = get_db_connection()
    c = conn.cursor()
    parsed_start = parse_datetime(start_time)
    parsed_end = parse_datetime(end_time)
    c.execute("INSERT INTO schedule (event, start_time, end_time) VALUES (?, ?, ?)", (event, parsed_start, parsed_end))
    conn.commit()
    conn.close()
    print(f"Event scheduled: {event} from {parsed_start} to {parsed_end}")