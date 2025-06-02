# Simple To-Do App
A command-line to-do app built with Python to manage tasks with priorities, due dates, and categories.

## Features
- Add tasks with priorities (High/Medium/Low, enter H/M/L), optional due dates (HH:MM AM/PM DD-MM-YYYY), user-defined categories, and recurrence (None/Daily/Weekly/Monthly/Yearly, enter D/W/M/Y)
- Input due date/time via separate prompts for hour, minutes, AM/PM, day, month, and year
- Quick actions: press 't' at day prompt for today, or at year prompt for current year
- Edit task description, priority, due date, category, or recurrence with a sub-menu
- Manage categories (add, remove, list) with a dedicated menu; cannot remove categories with assigned tasks
- Mark tasks as completed or uncompleted, displayed as [X] or [ ], with new instances for recurring tasks
- View tasks sorted by priority (High > Medium > Low, default), due date (earliest first), or category (alphabetical)
- Filter tasks by completion status (all, incomplete, completed), category, or recurrence
- Delete tasks with priority-sorted view
- Cancel adding, editing, or deleting tasks with 'x' or Enter
- View tasks with a pause until Enter is pressed
- Save tasks to `tasks.txt` and categories to `categories.txt` for persistence

## How to Run
1. Install Python 3.x.
2. Clone this repo: `git clone https://github.com/Azzbo77/python-learning.git`
3. Navigate to the folder: `cd todo-app`
4. Run: `python todo.py`

## Future Improvements
- Add task reminders or notifications
- Support custom recurrence intervals