# Simple To-Do App
A command-line to-do app built with Python to manage tasks with priorities and due dates.

## Features
- Add tasks with priorities (High/Medium/Low, enter H/M/L) and optional due dates (HH:MM AM/PM DD-MM-YYYY)
- Input due date/time via separate prompts for hour, minutes, AM/PM, day, month, year
- Quick action: press 't' at day prompt to set due date to today
- Cancel adding or deleting tasks with 'x' or Enter
- View tasks with priorities and due dates, pauses until Enter is pressed
- Delete tasks (displays tasks without pause)
- Save tasks to `tasks.txt` for persistence

## How to Run
1. Install Python 3.x.
2. Clone this repo: `git clone https://github.com/Azzbo77/python-learning.git`
3. Navigate to the folder: `cd todo-app`
4. Run: `python todo.py`

## Future Improvements
- Sort tasks by priority (High > Medium > Low) or due date
- Allow editing task descriptions, priorities, or due dates
- Add task categories (e.g., Work, Personal)
- Mark tasks as completed