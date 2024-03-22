import prompt_toolkit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession
import re
import requests
import json
import threading
import sys

# Define the Ollama API endpoint
url = 'https://api.ollama.com/v1/predict'

def get_user_input():
    # Get user input and return it as a string
    session = PromptSession()
    return session.prompt('> ', key_bindings=kb)

def predict(text):
    # Send the user's input to the Ollama API and print the response
    data = {'text': text}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_json = json.loads(response.content)
    print('OLLAMA:', response_json['predictions'][0]['label'])

def display_tasks():
    # Display the list of tasks as a numbered list
    for i, task in enumerate(tasks):
        print(f'{i+1}. {task.name}: {task.description}')

def complete_task(index):
    # Mark the specified task as completed and update the list of tasks
    tasks[index-1].complete = True
    display_tasks()

def remove_task(index):
    # Remove the specified task from the list of tasks
    del tasks[index-1]
    display_tasks()

def save_tasks():
    # Save the list of tasks to disk
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

def load_tasks():
    # Load the list of tasks from disk
    global tasks
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
        display_tasks()

# Define a key binding for Ctrl+S to save the list of tasks
kb = KeyBindings()
@kb.add('c-s')
def save_cb(event):
    save_tasks()

# Load the list of tasks from disk
load_tasks()

# Start a thread to read user input and send it to the Ollama API
Thread(target=predict, args=(get_user_input(),)).start()

# Handle task management commands in a loop
while True:
    # Display the prompt and get user input
    text = sys.stdin.readline().strip()

    # Split the user's input into commands and arguments
    words = text.split()
    command = words[0].lower()
    args = words[1:]

    # Handle task management commands
    if command == 'tasks':
        display_tasks()
    elif command == 'add':
        tasks.append(Task(*args))
        save_tasks()
    elif command == 'complete':
        complete_task(int(args[0]))
    elif command == 'remove':
        remove_task(int(args[0]))
    # Handle help requests
    elif command == 'help' or command == '?':
        print('Commands:')
        print('  ollama <text>: Send text to the Ollama API for
prediction')
        print('  tasks: Display the list of tasks')
        print('  add <name> <description>: Add a new task to the list')
        print('  complete <index>: Mark a task as completed')
        print('  remove <index>: Remove a task from the list')
        print('  save: Save the list of tasks to disk')
        print('  load: Load the list of tasks from disk')
        print('  help: Display this help message')
    # Handle exit requests
    elif command == 'exit':
        break
    # Handle unknown commands
    else:
        print(f'Unknown command {command}')