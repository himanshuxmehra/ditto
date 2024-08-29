from database.db_operations import get_db_connection
from utils.date_utils import parse_date

def add_reminder(text, date):
    conn = get_db_connection()
    c = conn.cursor()
    parsed_date = parse_date(date)
    c.execute("INSERT INTO reminders (text, date) VALUES (?, ?)", (text, parsed_date))
    conn.commit()
    conn.close()
    print(f"Reminder added: {text} on {parsed_date}")