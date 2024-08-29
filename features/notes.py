from database.db_operations import get_db_connection
from datetime import datetime

def add_note(title, content):
    conn = get_db_connection()
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO notes (title, content, date) VALUES (?, ?, ?)", (title, content, date))
    conn.commit()
    conn.close()
    print(f"Note added: {title}")

def view_notes():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    rows = c.fetchall()
    conn.close()
    print(f"Notes:")
    for row in rows:
        print(f"{row[0]}: {row[1]}")

def delete_note(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    print(f"Note deleted: {id}")