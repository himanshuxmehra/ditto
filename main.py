import threading
from database.db_operations import init_db
from features.user_info import get_user_info, collect_user_info
from assistants.llm_assistant import LLMAssistant
from utils.reminders_service import start_reminder_service

def main():
    init_db()
    user_info = get_user_info()
    
    if not user_info:
        user_info = collect_user_info()
        print(f"Nice to meet you, {user_info['name']}! I'll remember this information to assist you better.")
    else:
        print(f"Welcome back, {user_info['name']}! How can I assist you today?")
    
    assistant = LLMAssistant(user_info)

    # Start reminder notification service in a separate thread
    reminder_thread = threading.Thread(target=start_reminder_service, daemon=True)
    reminder_thread.start()
    
    while True:
        user_input = input("> ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
        
        assistant.process_input(user_input)

if __name__ == "__main__":
    main()