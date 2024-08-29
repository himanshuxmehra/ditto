import time
import schedule
from database.db_operations import get_db_connection
from plyer import notification

def check_reminders():
    conn = get_db_connection()
    c = conn.cursor()
    current_time = time.strftime('%Y-%m-%d %H:%M')
    c.execute("SELECT text FROM reminders WHERE date = ?", (current_time,))
    reminders = c.fetchall()
    # print(reminders)
    for reminder in reminders:
        print("\nReminder: " + reminder[0] + "\n")
        # notify(reminder[0])
    conn.close()

def notify(reminder_text):
    notification.notify(
        title="Reminder",
        message=reminder_text,
        app_icon = None,
        timeout=10
    )

def start_reminder_service():
    schedule.every(1).minutes.do(check_reminders)
    while True:
        schedule.run_pending()
        time.sleep(1)
