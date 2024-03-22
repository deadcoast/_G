from prompt_toolkit.eventloop.typing import Event
from random import random
from sys import stdin
import re
from task5 import get_prediction, validate_input
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession

import requests
import json
import curses

# Initialize the curses window
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(False)
sh, sw = stdscr.getmaxyx()

# Define some colors for visual effects
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Create a dynamic greeting message
greeting = "  __     ______   ____  ___  \n |  |_  / ___/  | / /  \ 'Welcome to the Ollama CLI!'\_\ \n |       \\__ \\  |/ /__/\ /_/ \n |  _    ___) |    \/\n|_,/_./____(_)\/\_\  "
greeting_window = curses.newwin(sh, sw, 0, 0)
greeting_window.addstr(greeting, curses.color_pair(1))
greeting_window.refresh()

# Wait for a random amount of time before continuing
wait_time = random.uniform(0.5, 2)
curses.napms(int(wait_time * 1000))

# Define the key bindings
kb = KeyBindings()
@kb.add('c-s')
def save_cb(event):
    """
    Save the tasks to a file and exit the CLI.
    """
    try:
        save_tasks()
    except Exception as e:
        print(f'Error saving tasks: {str(e)}')
    finally:
        event.cli.exit()

kb = KeyBindings()

@kb.add('c-q')
def exit_cb(event: Event) -> None:
    """
    Exit the command line interface.
    """
    try:
        event.cli.exit()
    except Exception as e:
        print(f"Error occurred while exiting: {e}")
    return None

@kb.add('home')
def move_cursor_to_beginning(event):
    """
    Moves the cursor to the beginning of the line.
    """
    try:
        if event.cli is not None:
            event.cli.current_column = 0
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

@kb.add('end')
def move_cursor_to_end(event):
    """
    Move the cursor to the end of the line.
    """
    if event is not None:
        try:
            event.current_buffer.cursor_position = len(event.current_buffer.text)
        except Exception as e:
            print(f"An error occurred: {e}")

@kb.add('ctrl-x')
def delete_char(event):
    try:
        cursor_position = event.cli.get_cursor_position()
        del event.app.current_buffer[cursor_position.column]
    except Exception as e:
        print(f"An error occurred: {e}")

@kb.add('c-f')
def move_cursor_right(event):
    event.cli.current_column += 1

@kb.add('c-b')
def move_cursor_left(event):

    url = 'https://api.ollama.com/v1/predict'

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
        print('  ollama <text>: Send text to the Ollama API for prediction')
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
# Define keybindings
kb = KeyBindings()



# Create a PromptSession instance with the keybindings
session = PromptSession(key_bindings=kb)

# Display the prompt and get user input
user_input = session.prompt('Enter your command: ')
def ollama_cli():
    # Initialize the curses window
    stdscr = curses.initscr()
    curses.noecho()
    curses.curs_set(False)
    sh, sw = stdscr.getmaxyx()

    # Define some colors for visual effects
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Create a dynamic greeting message
    greeting = "  __     ______   ____  ___  \n |  |_  / ___/  | / /  \ 'Welcome to the Ollama CLI!'\_\ \n |       \\__ \\  |/ /__/\ /_/ \n |  _    ___) |    \/\n|_,/_./____(_)\/\_\  "
    greeting_window = curses.newwin(sh, sw, 0, 0)
    greeting_window.addstr(greeting, curses.color_pair(1))
    greeting_window.refresh()

    # Wait for a random amount of time before continuing
    wait_time = random.uniform(0.5, 2)
    curses.napms(int(wait_time * 1000))

    # Display the main menu options
    options = ["Create a new task", "View existing tasks", "Exit"]
    for i, option in enumerate(options):
        stdscr.addstr(i + 1, (sw // 2) - len(option) // 2, option, curses.color_pair(2))

    # Wait for user input and handle the selection
    while True:
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN]:
            # Handle arrow key events to navigate between options
            current_option = (stdscr.inch(stdscr.cury, 0) - ord('1')) // len(options[0])
            if key == curses.KEY_UP and current_option > 0:
                stdscr.addstr(current_option + 1, 0, ' ', curses.color_pair(1))
                stdscr.addstr(current_option, 0, options[current_option - 1], curses.color_pair(2))
            elif key == curses.KEY_DOWN and current_option < len(options) - 1:
                stdscr.addstr(current_option + 1, 0, ' ', curses.color_pair(1))
                stdscr.addstr(current_option + 2, 0, options[current_option + 1], curses.color_pair(2))
        elif key == curses.KEY_ENTER or key in [ord('1'), ord('2'), ord('3')]:
            stdscr.stdin.addstr(stdin.cury, 0, ' ', curses.color_pair(1))

            if key == ord('1'):
                stdscr.addstr(sh // 2, (sw // 2) - len("Enter your new task:"), "Enter your new task:",
                              curses.color_pair(2))
                name = stdscr.getstr((sh // 2) + 1, (sw // 2) - len("Your task description:"))

                stdscr.addstr(sh // 2 + 2, (sw // 2) - len("Enter your task description:"),
                              "Enter your task description:", curses.color_pair(2))
                description = stdscr.getstr((sh // 2) + 3, (sw // 2))

                tasks.append(Task(name, description))

                stdscr.addstr(sh // 2 + 4, (sw // 2) - len("Task created!") // 2, "Task created!", curses.color_pair(2))

            elif key == ord('2'):
                for i, task in enumerate(tasks):
                    stdscr.addstr((sh // 2) + i - 1, (sw // 2) - len(task.name),
                                  f"{i + 1}. {task.name}: {task.description}", curses.color_pair(2))

            elif key == ord('3'):
                break

    stdscr.keypad(False)
    curses.endwin()
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
    event = session.get_current_event()
    if event is not None:
        event.cli.handle_key_event(event)
        continue

    # Call complete_task or get_prediction depending on the user's input
    if user_input == 'tasks':
        display_tasks(tasks)
    elif re.match(r'^complete (\d+)$', user_input):
        complete_task(tasks)
    else:
        text = ' '.join(event.current_buffer)
        get_prediction(text)

if __name__ == "__main__":
    ollama_cli()