# Simple To-Do App
import os
from datetime import datetime

# Initialize tasks list
tasks = []

# Load tasks from file
def load_tasks():
    global tasks
    tasks = []
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.rsplit(" | ", 2)
                    task = parts[0]
                    priority = parts[1] if len(parts) > 1 else "Medium"
                    due_date = parts[2] if len(parts) == 3 else ""
                    tasks.append({"task": task, "priority": priority, "due_date": due_date})
        save_tasks()  # Update file format
    print("Tasks loaded from tasks.txt")

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            due_date = task["due_date"] if task["due_date"] else ""
            f.write(f"{task['task']} | {task['priority']} | {due_date}\n")

# Validate date/time components
def is_valid_datetime(hour, minutes, am_pm, day, month, year):
    if not all([hour, minutes, am_pm, day, month, year]):
        return True  # Allow partial or empty input
    try:
        datetime.strptime(f"{hour}:{minutes} {am_pm} {day}-{month}-{year}", "%I:%M %p %d-%m-%Y")
        return True
    except ValueError:
        return False

def add_task(task, priority, due_date):
    tasks.append({"task": task, "priority": priority, "due_date": due_date})
    due_date_display = f", Due: {due_date}" if due_date else ""
    print(f"Added task: {task} (Priority: {priority}{due_date_display})")
    save_tasks()

def view_tasks(pause=True):
    if not tasks:
        print("No tasks yet!")
    else:
        print("Your tasks:")
        for i, task in enumerate(tasks, 1):
            due_date_display = f", Due: {task['due_date']}" if task["due_date"] else ""
            print(f"{i}. {task['task']} (Priority: {task['priority']}{due_date_display})")
    if pause:
        input("Press Enter to continue...")

def delete_task(index):
    try:
        task = tasks.pop(index - 1)
        due_date_display = f", Due: {task['due_date']}" if task["due_date"] else ""
        print(f"Deleted task: {task['task']} (Priority: {task['priority']}{due_date_display})")
        save_tasks()
    except IndexError:
        print("Invalid task number!")

# Load tasks at startup
load_tasks()

# Main loop
while True:
    print("\nTo-Do App")
    print("1. Add task")
    print("2. View tasks")
    print("3. Delete task")
    print("4. Exit")
    choice = input("Choose an option (1-4): ").strip()

    if choice == "1":
        task = input("Enter task (press x to cancel): ").strip()
        if task.lower() == "x" or task == "":
            print("Task addition canceled.")
        else:
            priority = input("Enter priority (High/Medium/Low, enter H/M/L): ").strip().upper()
            priority_map = {"H": "High", "M": "Medium", "L": "Low"}
            if priority not in priority_map:
                print("Invalid priority! Defaulting to Medium.")
                priority = "Medium"
            else:
                priority = priority_map[priority]
            due_date = ""
            # Time input
            hour = input("Select hour (1-12, press x or Enter to cancel): ").strip()
            if hour.lower() == "x" or hour == "":
                due_date = ""
            else:
                try:
                    hour = int(hour)
                    if not 1 <= hour <= 12:
                        raise ValueError
                except ValueError:
                    print("Invalid hour! Skipping due date.")
                    due_date = ""
                else:
                    minutes = input("Select minutes (0-59, press x or Enter to cancel): ").strip()
                    if minutes.lower() == "x" or minutes == "":
                        due_date = ""
                    else:
                        try:
                            minutes = int(minutes)
                            if not 0 <= minutes <= 59:
                                raise ValueError
                            minutes = f"{minutes:02d}"
                        except ValueError:
                            print("Invalid minutes! Skipping due date.")
                            due_date = ""
                        else:
                            am_pm = input("Select AM or PM (press x or Enter to cancel): ").strip().upper()
                            if am_pm.lower() == "x" or am_pm == "":
                                due_date = ""
                            elif am_pm not in ["AM", "PM"]:
                                print("Invalid AM/PM! Skipping due date.")
                                due_date = ""
                            else:
                                # Date input
                                day = input("Select day (1-31, press t for today, x to cancel): ").strip()
                                if day.lower() == "x" or day == "":
                                    due_date = f"{hour}:{minutes} {am_pm}"
                                elif day.lower() == "t":
                                    today = datetime.now()
                                    day = f"{today.day:02d}"
                                    month = f"{today.month:02d}"
                                    year = str(today.year)
                                    if is_valid_datetime(hour, minutes, am_pm, day, month, year):
                                        due_date = f"{hour}:{minutes} {am_pm} {day}-{month}-{year}"
                                    else:
                                        print("Invalid date/time! Skipping due date.")
                                        due_date = ""
                                else:
                                    try:
                                        day = int(day)
                                        if not 1 <= day <= 31:
                                            raise ValueError
                                        day = f"{day:02d}"
                                    except ValueError:
                                        print("Invalid day! Using time only.")
                                        due_date = f"{hour}:{minutes} {am_pm}"
                                    else:
                                        month = input("Select month (1-12, press x or Enter to cancel): ").strip()
                                        if month.lower() == "x" or month == "":
                                            due_date = f"{hour}:{minutes} {am_pm}"
                                        else:
                                            try:
                                                month = int(month)
                                                if not 1 <= month <= 12:
                                                    raise ValueError
                                                month = f"{month:02d}"
                                            except ValueError:
                                                print("Invalid month! Using time only.")
                                                due_date = f"{hour}:{minutes} {am_pm}"
                                            else:
                                                year = input("Select year (e.g., 2025, press x or Enter to cancel): ").strip()
                                                if year.lower() == "x" or year == "":
                                                    due_date = f"{hour}:{minutes} {am_pm}"
                                                else:
                                                    try:
                                                        year = int(year)
                                                        if not 2000 <= year <= 2099:
                                                            raise ValueError
                                                    except ValueError:
                                                        print("Invalid year! Using time only.")
                                                        due_date = f"{hour}:{minutes} {am_pm}"
                                                    else:
                                                        if is_valid_datetime(hour, minutes, am_pm, day, month, year):
                                                            due_date = f"{hour}:{minutes} {am_pm} {day}-{month}-{year}"
                                                        else:
                                                            print("Invalid date/time! Skipping due date.")
                                                            due_date = ""
            add_task(task, priority, due_date)
    elif choice == "2":
        view_tasks(pause=True)
    elif choice == "3":
        view_tasks(pause=False)
        index = input("Enter task number to delete (press x to cancel): ").strip()
        if index.lower() == "x" or index == "":
            print("Task deletion canceled.")
        else:
            try:
                index = int(index)
                delete_task(index)
            except ValueError:
                print("Invalid input! Please enter a number or 'x'.")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")