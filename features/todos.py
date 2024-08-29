from database.db_operations import get_db_connection
from config import OLLAMA_API_URL
import requests
import json

def add_todo(task):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO todos (task, status) VALUES (?, ?)", (task, "pending"))
    conn.commit()
    conn.close()
    print(f"Todo added: {task}")

def view_todos():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM todos")
    todos = c.fetchall()
    conn.close()
    if todos:
        print("Your todos:")
        for todo in todos:
            print(f"ID: {todo[0]}, Task: {todo[1]}, Status: {todo[2]}")
    else:
        print("You have no todos.")

def complete_todo(todo_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE todos SET status = 'completed' WHERE id = ?", (todo_id,))
    if c.rowcount == 0:
        print(f"No todo found with ID {todo_id}")
    else:
        print(f"Todo {todo_id} marked as completed")
    conn.commit()
    conn.close()

def delete_todo(todo_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if c.rowcount == 0:
        print(f"No todo found with ID {todo_id}")
    else:
        print(f"Todo {todo_id} deleted")
    conn.commit()
    conn.close()

def get_pending_todos():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM todos WHERE status = 'pending'")
    todos = c.fetchall()
    conn.close()
    return todos

def suggest_priority_tasks(user_info):
    todos = get_pending_todos()
    todo_list = [todo[1] for todo in todos]  # Extract task descriptions
    
    prompt = f"""
    Given the user's information and their current pending tasks, suggest which tasks they should prioritize and why. Provide a brief explanation for each suggestion.

    User Information:
    {json.dumps(user_info, indent=2)}

    Pending Tasks:
    {json.dumps(todo_list, indent=2)}

    Please provide your suggestions in the following format:
    1. [Task]: [Reason for prioritization]
    2. [Task]: [Reason for prioritization]
    ...

    Limit your response to the top 3 priority tasks.
    """
    
    data = {
        "model": "llama2",
        "prompt": prompt
    }
    response = requests.post(OLLAMA_API_URL, json=data)
    return response.json()['response']