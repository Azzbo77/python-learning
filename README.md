# Simple To-Do App
A command-line to-do app built with Python to manage tasks with priorities, due dates, and categories.

## Features
- Add tasks with priorities (High/Medium/Low, enter H/M/L), optional due dates (HH:MM AM/PM DD-MM-YYYY), and user-defined categories
- Input due date/time via separate prompts for hour, minutes, AM/PM, day, month, and year
- Quick actions: press 't' at day prompt for today, or at year prompt for current year
- Edit task description, priority, due date, or category with a sub-menu
- Manage categories (add, remove, list) with a dedicated menu
- View tasks unsorted or sorted by priority (High > Medium > Low), due date (earliest first, displays due date before priority), or category (alphabetical)
- Delete tasks with default (unsorted) view, no sorting prompt
- Cancel adding, editing, or deleting tasks with 'x' or Enter
- View tasks with a pause until Enter is pressed
- Save tasks to `tasks.txt` and categories to `categories.txt` for persistence

## How to Run
1. Install Python 3.x.
2. Clone this repo: `git clone https://github.com/Azzbo77/python-learning.git`
3. Navigate to the folder: `cd todo-app`
4. Run: `python todo.py`

## Future Improvements
- Mark tasks as completed
- Add recurring tasks