import prompt_toolkit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession
import re
import requests

# Define the Ollama API endpoint
url = 'https://api.ollama.com/v1/predict'

def get_user_input():
    # Get user input and return it as a string
    session = PromptSession()
    return session.prompt('> ')

def predict(text):
    # Send a request to the Ollama API with the user's input
    data = {'text': text}
    response = requests.post(url, json=data)

    # Extract the prediction result from the API response
    if response.status_code == 200:
        result = response.json()['result']
    else:
        print('Error: Failed to get a prediction')
        return None

    return result

def display_tasks(tasks):
    # Display the list of tasks in a user-friendly format
    for i, task in enumerate(tasks):
        status = '[x]' if task.completed else '[ ]'
        print(f'{i+1}. {status} {task.name}: {task.description}')

def validate_input(user_input):
    # Validate the user's input and return True if it's valid, or False
otherwise
if not user_input:
    print('Error: Input cannot be empty')
    # Example regular expression to check for a valid email address
if re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', user_input) is None:
    print('Error: Invalid email address format')

def complete_task(tasks):
    # Allow the user to mark a task as complete using keyboard shortcuts
    display_tasks(tasks)
    user_input = input('Enter a command (e.g. "complete 1"): ')
    command, arg = user_input.split(' ')
    if command == 'complete':
        task_index = int(arg) - 1
        if 0 <= task_index < len(tasks):
            tasks[task_index].completed = True
        else:
            print('Error: Invalid task index')

def get_prediction(text):
    # Send the user's input for prediction using Ollama
    result = predict(text)
    if result is not None:
        print(f'Predicted: {result}')

# Define keybindings
kb = KeyBindings()

@kb.add('c-n')
def move_cursor_down(event):
    event.cli.current_line += 1

@kb.add('c-p')
def move_cursor_up(event):
    event.cli.current_line -= 1

@kb.add('c-b')
def move_cursor_left(event):
    event.cli.current_column -= 1

@kb.add('c-f')
def move_cursor_right(event):
    event.cli.current_column += 1

@kb.add('c-d')
def delete_char(event):
    del event.current_buffer[event.current_column - 1]

@kb.add('c-a')
def move_cursor_to_beginning(event):
    event.cli.current_column = 0

@kb.add('c-e')
def move_cursor_to_end(event):
    event.cli.current_column = len(event.current_buffer)

@kb.add('enter')
def enter_key(event):
    # Handle the Enter key by calling get_prediction with the user's input
    text = ' '.join(event.current_buffer)
    get_prediction(text)
    event.cli.reset()

# Define a Task class to represent individual tasks in our to-do list
class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.completed = False

# Initialize the list of tasks and the main loop
tasks = [
    Task('Buy groceries', 'Milk, eggs, bread, etc.'),
    Task('Do laundry', 'Wash, dry, fold'),
]
session = PromptSession(key_bindings=kb)

while True:
    # Display the prompt and get user input
    user_input = get_user_input()

    # Validate the user's input and exit the loop if it's not valid
    if not validate_input(user_input):
        continue

    # Handle keyboard shortcuts for navigating and editing the command
line
    event = session.get_current_event()
    if event is not None:
        event.cli.handle_key_event(event)
        

    # Call complete_task or get_prediction depending on the user's input
    if user_input == 'tasks':
        display_tasks(tasks)
    elif re.match(r'^complete (\d+)$', user_input):
        complete_task(tasks)
    else:
        text = ' '.join(event.current_buffer)
        get_prediction(text)