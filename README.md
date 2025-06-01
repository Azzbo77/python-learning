# Simple To-Do App
A command-line to-do app built with Python to manage tasks with priorities and due dates.

## Features
- Add tasks with priorities (High/Medium/Low, enter H/M/L) and optional due dates (HH:MM AM/PM DD-MM-YYYY)
- Input due date/time via separate prompts for hour, minutes, AM/PM, day, month, and year
- Quick actions: press 't' at day prompt for today, or at year prompt for current year
- View tasks unsorted or sorted by priority (High > Medium > Low) or due date (earliest first, displays due date before priority)
- Delete tasks with default (unsorted) view, no sorting prompt
- Cancel adding or deleting tasks with 'x' or Enter
- View tasks with a pause until Enter is pressed
- Delete tasks (displays tasks without pause)
- Save tasks to `tasks.txt` for persistence

## How to Run
1. Install Python 3.x.
2. Clone this repo: `git clone https://github.com/Azzbo77/python-learning.git`
3. Navigate to the folder: `cd todo-app`
4. Run: `python todo.py`

## Future Improvements
- Allow editing task descriptions, priorities, or due dates
- Add task categories (e.g., Work, Personal)
- Mark tasks as completed