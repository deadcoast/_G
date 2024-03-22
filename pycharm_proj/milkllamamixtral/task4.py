import prompt_toolkit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession
import re
import requests
import json

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
    task = tasks[index-1]
    task.completed = True
    display_tasks()

def add_task():
    # Add a new task to the list of tasks
    name = get_user_input('Enter task name: ')
    description = get_user_input('Enter task description: ')
    tasks.append(Task(name, description))

def remove_task():
    # Remove the specified task from the list of tasks
    index = int(get_user_input('Enter task number to remove: ')) - 1
    del tasks[index]

def save_tasks():
    # Save the list of tasks to a file
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

def load_tasks():
    # Load the list of tasks from a file
    try:
        with open('tasks.json', 'r') as f:
            tasks = [Task(**task) for task in json.load(f)]
    except FileNotFoundError:
        pass

# Initialize the list of tasks and load any existing tasks from disk
load_tasks()

# Define a Task class to represent individual tasks in our to-do list
class Task:
    def __init__(self, name, description, completed=False):
        self.name = name
        self.description = description
        self.completed = completed

# Define the key bindings for navigating and editing the command line
kb = KeyBindings()
kb.add('tab')(lambda event: event.cli.complete_next())
kb.add('ctrl+a')(lambda event: event.cli.move_to_start_of_line())
kb.add('ctrl+e')(lambda event: event.cli.move_to_end_of_line())
kb.add('ctrl+u')(lambda event:
event.cli.delete_from_cursor_to_start_of_line())
kb.add('ctrl+k')(lambda event:
event.cli.delete_from_cursor_to_end_of_line())
kb.add('ctrl+w')(lambda event: event.cli.delete_previous_word())
kb.add('enter')(predict)

# Define the main loop for the Milky CLI
while True:
    # Display the prompt and get user input
    text = get_user_input().strip()

    # Check if the user wants to exit the CLI
    if text == 'exit':
        break

    # Split the user's input into commands and arguments
    words = text.split()
    command = words[0].lower()
    args = words[1:]

    # Handle Ollama API requests
    if command == 'ollama' or command == '':
        predict(' '.join(args))

    # Handle task management commands
    elif command == 'tasks':
        display_tasks()
    elif command == 'add':
        add_task()
    elif command == 'complete':
        complete_task(int(args[0]))
    elif command == 'remove':
        remove_task()
    elif command == 'save':
        save_tasks()
    elif command == 'load':
        load_tasks()

    # Handle help requests
    elif command == 'help' or command == '?':
        print('Commands:')
        print('  ollama <text>: Send text to the Ollama API for
prediction')
        print('  tasks: Display the list of tasks')
        print('  add: Add a new task to the list')
        print('  complete <index>: Mark a task as completed')
        print('  remove <index>: Remove a task from the list')
        print('  save: Save the list of tasks to disk')
        print('  load: Load the list of tasks from disk')
        print('  help: Display this help message')
        print('  exit: Exit the Milky CLI')
    else:
        print(f'Unknown command {command}')

# Save the list of tasks to disk before exiting
save_tasks()