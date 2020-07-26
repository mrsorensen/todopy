import curses
import json
import os
import random


# CONFIG -------------------
todojson = 'todos.json'
# END - CONFIG ------------


# Main
def main(s):
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    
    # inp = s.getch()
    # s.addstr(0,0,str(inp))
    # s.getch()
    run(s)

def run(s):
    current_choice = 0
    h, w = s.getmaxyx()
    start = 0
    end = h-3


    while True:
        nh, nw = s.getmaxyx()
        if nh != h:
            start = 0
            end = nh-3
        todos = get_todos()
        clear(s)
        print_todos(s, current_choice, start, end)
        key = s.getch()

        # Move down
        if (key == curses.KEY_DOWN or key == 106) and current_choice < len(todos)-1:
            if current_choice > end - 3:
                start += 1
                end += 1
            current_choice += 1
        # Move up
        elif (key == curses.KEY_UP or key == 107) and current_choice > 0:
            if current_choice < start + 2:
                if start > 0:
                    start -= 1
                    end -= 1
            current_choice -= 1
        # Add todo
        elif key == 97:
            user_input = get_user_input(s, len(todos)+5)
            if len(user_input) > 0:
                add_todo(user_input)
        # Toggle todo
        elif key == 32 or key == 13 or key == 10:
            toggle_todo(current_choice)
        # Delete todo
        elif key == 127 or key == 330 or key == 100:
            delete_todo(s, current_choice)
            if current_choice > 0 and current_choice == len(todos) -1:
                current_choice -= 1

def count_completed(todos):
    completed = []
    for todo in todos:
        if todo['completed'] == 'true':
            completed.append(todo)
    return len(completed)

def delete_todo(s, current_choice):
    todos = get_todos()
    del todos[current_choice]
    store_todos(todos)

def toggle_todo(current_choice):
    todos = get_todos()
    if todos[current_choice]['completed'] == 'false':
        todos[current_choice]['completed'] = 'true'
    else:
        todos[current_choice]['completed'] = 'false'
    store_todos(todos)

def add_todo(todo):
    todos = get_todos()
    todos.append({
        'objective': todo.decode('utf-8'),
        'completed': 'false'
        })
    store_todos(todos)

def get_user_input(s, line):
    h, w = s.getmaxyx()
    s.addstr(h-1, 0, ' New todo:  ', curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE)
    curses.echo()
    curses.curs_set(1)
    user_input = s.getstr(h-1, 11)

    curses.curs_set(0)
    curses.noecho()
    if user_input == '':
        return 0
    else:
        return user_input


def print_todos(s, current_choice, start, end):

    h, w = s.getmaxyx()
    if current_choice >= start:
        current_choice = current_choice - start

    todos = get_todos()

    s.addstr(0, 0, 'Todos:' + '    ' + str(start + current_choice + 1) + '/' + str(len(todos)), curses.A_BOLD)
    s.addstr(h-2, 0, 'Completed: ' + str(count_completed(todos)) + '/' + str(len(todos)))


    if todos:
        for idx, todo in enumerate(todos[start:end]):
            if idx == current_choice:
                if todo['completed'] == 'false':
                    s.addstr(idx+1, 0, ' [ ] ' + todo['objective'] + ' ',curses.color_pair(1) | curses.A_REVERSE)
                else:
                    s.addstr(idx+1, 0, ' [X] ' + todo['objective'] + ' ', curses.color_pair(2) | curses.A_REVERSE)
            else:
                if todo['completed'] == 'false':
                    s.addstr(idx+1, 0, ' [ ] ' + todo['objective'] + ' ', curses.color_pair(1))
                else:
                    s.addstr(idx+1, 0, ' [X] ' + todo['objective'] + ' ', curses.color_pair(2))
    else:
        s.addstr(2, 0, 'No todos. Press \'a\' to add a new todo.')


# Return List of all todos from file
def get_todos():
    verify_todo_file()
    pwd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(pwd, todojson)) as f:
        data = json.load(f)
        return sorted(data, key=lambda x : x['completed'], reverse=False)


# Create todo file if it doesn't exist
def verify_todo_file():
    pwd = os.path.dirname(os.path.realpath(__file__))
    todo_file = os.path.join(pwd, todojson)
    if not os.path.isfile(todo_file):
        # os.mknod(os.path.join(pwd, todojson))
        with open(os.path.join(pwd, todojson), 'w+') as f:
            f.write('[]')

def store_todos(todos):
    pwd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(pwd, todojson), 'w') as f:
        json.dump(todos, f, indent=2)

def clear(s):
    s.erase()

def fill_todos():

    for _ in range(0, 60):
        todo = random.randint(100000, 999999)
        add_todo(str(todo).encode('utf-8'))


curses.wrapper(main)

# verify_todo_file(todojson)
