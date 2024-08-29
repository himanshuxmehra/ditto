import json
import requests
from config import OLLAMA_API_URL
from assistants.base_assistant import BaseAssistant
from features import reminders, notes, schedule, todos, user_info
from utils.date_utils import parse_date  

class LLMAssistant(BaseAssistant):
    def sendRequest(self, prompt):
        data = {
            "model": "llama3",
            "prompt": prompt,
            "stream": True
        }
        r = requests.post(OLLAMA_API_URL, json=data, stream=True)
        r.raise_for_status()
        output = ""
        message = ""
        for line in r.iter_lines():
            body = json.loads(line)
            if "error" in body:
                raise Exception(body["error"])
            if body["done"] != True:
                message += body["response"]
                # the response streams one token at a time, print that as we receive it
            if body["done"]==True: 
                # print(message)
                return message

    def query_llm(self, prompt):
        response = self.sendRequest(prompt)
        return response


    def interpret_input(self, user_input):
        prompt = f"""
        Given the user information and the following input, interpret the user's intent and categorize it as one of these actions: REMIND, NOTE, SCHEDULE, TODO, VIEW_TODOS, COMPLETE_TODO, DELETE_TODO, UPDATE_INFO, SUGGEST_PRIORITIES, or UNKNOWN.
        For REMIND, extract the reminder text and the exact time expression used (e.g., "in 5 minutes", "tomorrow at 3pm").
        For NOTE, extract the title and content.
        For SCHEDULE, extract the event name, start time, and end time. Provide the exact time expressions used.
        For TODO, extract the task.
        For COMPLETE_TODO or DELETE_TODO, extract the todo ID.
        For UPDATE_INFO, identify which user information field needs to be updated.
        For SUGGEST_PRIORITIES, no additional information is needed.
        
        User input: "{user_input}"
        
        Your response must be in valid JSON format as shown below. Do not include any other text outside the JSON structure.
        {{
            "action": "REMIND/NOTE/VIEW_NOTES/DELETE_NOTE/SCHEDULE/TODO/VIEW_TODOS/COMPLETE_TODO/DELETE_TODO/UPDATE_INFO/SUGGEST_PRIORITIES/UNKNOWN",
            "reminder_text": "",
            "reminder_date": "",
            "note_title": "",
            "note_content": "",
            "event_name": "",
            "event_start": "",
            "event_end": "",
            "todo_task": "",
            "todo_id": "",
            "update_field": "",
            "update_value": ""
        }}
        """
        response = self.query_llm(prompt)
        try:
            interpreted = json.loads(response)
            
            # Parse dates for reminders and schedules
            if interpreted['action'] == 'REMIND':
                interpreted['reminder_date'] = parse_date(interpreted['reminder_date'])
            elif interpreted['action'] == 'SCHEDULE':
                interpreted['event_start'] = parse_date(interpreted['event_start'])
                interpreted['event_end'] = parse_date(interpreted['event_end'])
            
            return interpreted
        except json.JSONDecodeError:
            print("Error: Unable to parse LLM response. Using fallback interpretation.")
            return {"action": "UNKNOWN"}
        except ValueError as e:
            print(f"Error: {str(e)}")
            return {"action": "UNKNOWN"}
    
    def process_input(self, user_input):
        interpreted = self.interpret_input(user_input)
        action = interpreted['action']

        if action == 'REMIND':
            reminders.add_reminder(interpreted['reminder_text'], interpreted['reminder_date'])
        elif action == 'NOTE':
            notes.add_note(interpreted['note_title'], interpreted['note_content'])
        elif action == 'VIEW_NOTES':
            notes.view_notes()
        elif action == 'VIEW_NOTES':
            notes.delete_note(interpreted['note_id'])
        elif action == 'SCHEDULE':
            schedule.add_schedule(interpreted['event_name'], interpreted['event_start'], interpreted['event_end'])
        elif action == 'TODO':
            todos.add_todo(interpreted['todo_task'])
        elif action == 'VIEW_TODOS':
            todos.view_todos()
        elif action == 'COMPLETE_TODO':
            todos.complete_todo(interpreted['todo_id'])
        elif action == 'DELETE_TODO':
            todos.delete_todo(interpreted['todo_id'])
        elif action == 'UPDATE_INFO':
            user_info.update_user_info(self.user_info, interpreted['update_field'], interpreted['update_value'])
        elif action == 'SUGGEST_PRIORITIES':
            suggestions = todos.suggest_priority_tasks(self.user_info)
            print("Here are my suggestions for task prioritization:")
            print(suggestions)
        else:
            print("I'm not sure what you want me to do. Can you please rephrase your request?")