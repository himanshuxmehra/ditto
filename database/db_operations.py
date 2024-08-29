import sqlite3
from config import DB_NAME

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY, text TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS schedule
                 (id INTEGER PRIMARY KEY, event TEXT, start_time TEXT, end_time TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS todos
                 (id INTEGER PRIMARY KEY, task TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_info
                 (id INTEGER PRIMARY KEY, info TEXT)''')
    conn.commit()
    conn.close()