# Define the Ollama API endpoint
url = 'https://api.ollama.com/v1/predict'


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


# Get user input and send it for prediction
user_input = input('Enter some text: ')
prediction = predict(user_input)
if prediction is not None:
    print(f'Predicted: {prediction}')


@kb.add('c-n')  # ##Ckeybind## Ctrl+N
def navigate_down(event):
    # TODO: Implement navigation down
    pass


@kb.add('c-p')  # ##Ckeybind## Ctrl+P
def navigate_up(event):
    # TODO: Implement navigation up
    pass


def validate_input(user_input):
    if not user_input:
        print('Error: Input cannot be empty')
        return False

    # Example regular expression to check for a valid email address
    if re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', user_input) is None:
        print('Error: Invalid email address format')
        return False

    # Additional validation logic can be added here as needed
    # ...

    return True


# Define the Ollama API endpoint
url = 'https://api.ollama.com/v1/predict'


def get_user_input():
    # Get user input and return it as a string
    session = PromptSession()
    user_input = session.prompt('> ')
    return user_input


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
        status = '[ ]' if not task.completed else '[x]'
        print(f'{i + 1}. {status} {task.name}: {task.description}')


def validate_input(user_input):


# Validate the user's input and return True if it's valid, or False
otherwise
if not user_input:
    print('Error: Input cannot be empty')
    return False

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


class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.completed = False

    def complete(self):
        self.completed = True


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


# Example tasks
task1 = Task('Buy groceries', 'Milk, eggs, bread')
task2 = Task('Walk the dog', '30 minutes in the park')

# Create a list to store the tasks
tasks = [task1, task2]


def display_tasks():
    for i, task in enumerate(tasks):
        status = '[ ]' if not task.completed else '[x]'
        print(f'{i + 1}. {status} {task.name}: {task.description}')

    # Example regular expression to check for a valid email address
    if re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', user_input) is None:
        print('Error: Invalid email address format')
        return False

    return True


# Define keybindings
kb = KeyBindings()


@kb.add('c-n')
def move_cursor_down(event):
    event.cli.current_line += 1


@kb.add('c-p')
def move_cursor_up(event):
    event.cli.current_line -= 1


@kb.add('c-e')
def complete_task(event):
    display_tasks()
    user_input = input('Enter a command (e.g. "complete 1"): ')
    command, arg = user_input.split(' ')
    if command == 'complete':
        task_index = int(arg) - 1
        if 0 <= task_index < len(tasks):
            tasks[task_index].complete()
        else:
            print('Error: Invalid task index')


# Display the tasks and get user input
display_tasks()
user_input = input('Enter a command (e.g. "complete 1"): ')
command, arg = user_input.split(' ')
if command == 'complete':
    task_index = int(arg) - 1
    if 0 <= task_index < len(tasks):
        tasks[task_index].complete()
    else:
        print('Error: Invalid task index')