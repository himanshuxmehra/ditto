def start_reminder_service():
    schedule.every(1).minutes.do(check_reminders)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_reminder_service()
