import json
from database.db_operations import get_db_connection

def get_user_info():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT info FROM user_info WHERE id = 1")
    result = c.fetchone()
    conn.close()
    if result:
        return json.loads(result[0])
    return None

def save_user_info(info):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO user_info (id, info) VALUES (1, ?)", (json.dumps(info),))
    conn.commit()
    conn.close()

def collect_user_info():
    user_info = {}
    user_info['name'] = input("What's your name? ")
    user_info['age'] = input("How old are you? ")
    user_info['occupation'] = input("What's your occupation? ")
    user_info['hobbies'] = input("What are some of your hobbies? (comma-separated) ").split(',')
    user_info['goals'] = input("What are some of your current goals? (comma-separated) ").split(',')
    save_user_info(user_info)
    return user_info

def update_user_info(user_info, field, value):
    user_info[field] = value
    save_user_info(user_info)
    print(f"Updated your {field} to {value}.")