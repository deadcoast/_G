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

class Task:
    # A class to represent a task
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.complete = False

def get_user_input():
    # Get user input and return it as a string
    session = PromptSession()
    text = session.prompt('> ', key_bindings=kb)
    return text

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
        print(f'{i+1}. {task.name}: {task.description} (completed:
{task.complete})')

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

def summarize_tasks():
    # Send all task descriptions to the Ollama API and print a summary
    text = '\n'.join([task.description for task in tasks if not
task.complete])
    data = {'text': text}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_json = json.loads(response.content)
    summary = ''
    for label in set(pred['label'] for pred in
response_json['predictions']):
        count = len([pred for pred in response_json['predictions'] if
pred['label'] == label])
        summary += f'{count} tasks related to {label}\n'
    print('OLLAMA: Task Summary\n' + summary)

# Define key bindings
kb = KeyBindings()
@kb.add('c-s')
def save(event):
    # Save the list of tasks to disk when Ctrl+S is pressed
    save_tasks()
@kb.add('c-q')
def quit(event):
    # Quit the program when Ctrl+Q is pressed
    sys.exit()
@kb.add('c-x')
def summarize(event):
    # Summarize the list of tasks when Ctrl+X is pressed
    summarize_tasks()

# Define a loop to handle user input
while True:
    # Get user input
    text = get_user_input()
    # Check for task-related commands
    if text.startswith('task '):
        command, *args = text[5:].split()
        if command == 'new':
            name, description = args
            tasks.append(Task(name, description))
        elif command == 'list':
            display_tasks()
        elif command == 'complete':
            try:
                index = int(args[0])
                complete_task(index)
            except ValueError:
                print('Invalid task number')
        elif command == 'remove':
            try:
                index = int(args[0])
                remove_task(index)
            except ValueError:
                print('Invalid task number')
    # Check for Ollama-related commands
    elif text.startswith('ollama '):
        command, *args = text[7:].split()
        if command == 'predict':
            data = {'text': args[0]}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data),
headers=headers)
            response_json = json.loads(response.content)
            print('OLLAMA:', response_json['predictions'][0]['label'])
        elif command == 'summarize':
            summarize_tasks()
    # Check for help commands
    elif text in {'help', '?'}:
        print('Available commands:\n'
              'task new <name> <description>: create a new task\n'
              'task list: display the list of tasks\n'
              'task complete <index>: mark a task as completed\n'
              'task remove <index>: remove a task\n'
              'ollama predict <text>: send text to the Ollama API for
prediction\n'
              'ollama summarize: summarize all tasks using the Ollama
API\n'
              'c-s: save tasks to disk\n'
              'c-q: quit the program\n'
              'c-x: summarize tasks using the Ollama API')
    # Check for exit commands
    elif text in {'bye', 'exit'}:
        break
    # Send input to the Ollama API
    else:
        threading.Thread(target=predict, args=(text,)).start()