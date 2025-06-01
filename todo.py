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
                    parts = line.rsplit(" | ", 3)
                    task = parts[0]
                    priority = parts[1] if len(parts) > 1 else "Medium"
                    due_date = parts[2] if len(parts) > 2 else ""
                    category = parts[3] if len(parts) > 3 else "Personal"
                    # Map invalid/old categories to Personal
                    category_map = {"W": "Work", "P": "Personal"}
                    category = category_map.get(category.upper(), "Personal") if category else "Personal"
                    tasks.append({"task": task, "priority": priority, "due_date": due_date, "category": category})
        save_tasks()  # Update file format
    print("Tasks loaded from tasks.txt")

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            due_date = task["due_date"] if task["due_date"] else ""
            f.write(f"{task['task']} | {task['priority']} | {due_date} | {task['category']}\n")

# Validate date/time components
def is_valid_datetime(hour, minutes, am_pm, day, month, year):
    if not all([hour, minutes, am_pm, day, month, year]):
        return True  # Allow partial or empty input
    try:
        datetime.strptime(f"{hour}:{minutes} {am_pm} {day}-{month}-{year}", "%I:%M %p %d-%m-%Y")
        return True
    except ValueError:
        return False

def add_task(task, priority, due_date, category):
    tasks.append({"task": task, "priority": priority, "due_date": due_date, "category": category})
    due_date_display = f", Due: {due_date}" if due_date else ""
    category_display = f", Category: {category}"
    print(f"Added task: {task} (Priority: {priority}{due_date_display}{category_display})")
    save_tasks()

def view_tasks(pause=True, default_view=False):
    if not tasks:
        print("No tasks yet!")
        if pause:
            input("Press Enter to continue...")
        return
    if default_view:
        tasks_to_view = tasks
        sort_method = ""
    else:
        priority_order = {"High": 2, "Medium": 1, "Low": 0}
        def get_due_date(task):
            if not task["due_date"]:
                return datetime.max  # No due date goes last
            try:
                return datetime.strptime(task["due_date"], "%I:%M %p %d-%m-%Y")
            except ValueError:
                return datetime.max  # Invalid or time-only due date goes last
        choice = input("View by: 1. Default 2. Priority (High > Medium > Low) 3. Due date (earliest first) 4. Category (press x to cancel): ").strip()
        if choice.lower() == "x" or choice == "":
            print("View canceled.")
            return
        tasks_to_view = tasks
        sort_method = ""
        if choice == "2":
            tasks_to_view = sorted(tasks, key=lambda x: priority_order[x["priority"]], reverse=True)
            sort_method = "priority"
        elif choice == "3":
            tasks_to_view = sorted(tasks, key=get_due_date)
            sort_method = "due date"
        elif choice == "4":
            tasks_to_view = sorted(tasks, key=lambda x: x["category"])
            sort_method = "category"
        elif choice != "1":
            print("Invalid choice!")
            return
    if sort_method:
        print(f"Tasks sorted by {sort_method}")
    print("Your tasks:")
    for i, task in enumerate(tasks_to_view, 1):
        due_date_display = f"Due: {task['due_date']}" if task['due_date'] else ""
        priority_display = f"Priority: {task['priority']}"
        category_display = f"Category: {task['category']}"
        if sort_method == "due date" and task["due_date"]:
            display = f"{category_display}, {due_date_display}, {priority_display}"
        else:
            display = f"{category_display}, {priority_display}{', ' + due_date_display if task['due_date'] else ''}"
        print(f"{i}. {task['task']} ({display})")
    if pause:
        input("Press Enter to continue...")

def delete_task(index):
    try:
        task = tasks.pop(index - 1)
        due_date_display = f", Due: {task['due_date']}" if task['due_date'] else ""
        category_display = f", Category: {task['category']}"
        print(f"Deleted task: {task['task']} (Priority: {task['priority']}{due_date_display}{category_display})")
        save_tasks()
    except IndexError:
        print("Invalid task number!")

def edit_task(index):
    try:
        task = tasks[index - 1]
        due_date_display = f", Due: {task['due_date']}" if task['due_date'] else ""
        category_display = f", Category: {task['category']}"
        print(f"Editing task: {task['task']} (Priority: {task['priority']}{due_date_display}{category_display})")
        choice = input("Edit: 1. Description 2. Priority 3. Due date 4. Category (press x to cancel): ").strip()
        if choice.lower() == "x" or choice == "":
            print("Edit canceled.")
            return
        if choice == "1":
            new_task = input("Enter new description (press x to cancel): ").strip()
            if new_task.lower() == "x" or new_task == "":
                print("Edit canceled.")
                return
            tasks[index - 1]["task"] = new_task
            print(f"Updated description to: {new_task}")
        elif choice == "2":
            priority = input("Enter new priority (High/Medium/Low, enter H/M/L): ").strip().upper()
            priority_map = {"H": "High", "M": "Medium", "L": "Low"}
            if priority not in priority_map:
                print("Invalid priority! Keeping original.")
                return
            tasks[index - 1]["priority"] = priority_map[priority]
            print(f"Updated priority to: {priority_map[priority]}")
        elif choice == "3":
            due_date = get_due_date()
            tasks[index - 1]["due_date"] = due_date
            due_date_display = f"Due: {due_date}" if due_date else "None"
            print(f"Updated due date to: {due_date_display}")
        elif choice == "4":
            category = input("Enter new category (Work/Personal, press Enter for Personal): ").strip()
            category_map = {"W": "Work", "P": "Personal"}
            category = category_map.get(category.upper(), "Personal") if category else "Personal"
            tasks[index - 1]["category"] = category
            print(f"Updated category to: Category: {category}")
        else:
            print("Invalid choice!")
            return
        save_tasks()
    except IndexError:
        print("Invalid task number!")

def get_due_date():
    due_date = ""
    hour = input("Select hour (1-12, press x or Enter to cancel): ").strip()
    if hour.lower() == "x" or hour == "":
        return due_date
    try:
        hour = int(hour)
        if not 1 <= hour <= 12:
            raise ValueError
    except ValueError:
        print("Invalid hour! Skipping due date.")
        return due_date
    minutes = input("Select minutes (0-59, press x or Enter to cancel): ").strip()
    if minutes.lower() == "x" or minutes == "":
        return due_date
    try:
        minutes = int(minutes)
        if not 0 <= minutes <= 59:
            raise ValueError
        minutes = f"{minutes:02d}"
    except ValueError:
        print("Invalid minutes! Skipping due date.")
        return due_date
    am_pm = input("Select AM or PM (press x or Enter to cancel): ").strip().upper()
    if am_pm.lower() == "x" or am_pm == "":
        return due_date
    if am_pm not in ["AM", "PM"]:
        print("Invalid AM/PM! Skipping due date.")
        return due_date
    day = input("Select day (1-31, press t for today, x to cancel): ").strip()
    if day.lower() == "x" or day == "":
        return f"{hour}:{minutes} {am_pm}"
    if day.lower() == "t":
        today = datetime.now()
        day = f"{today.day:02d}"
        month = f"{today.month:02d}"
        year = str(today.year)
    else:
        try:
            day = int(day)
            if not 1 <= day <= 31:
                raise ValueError
            day = f"{day:02d}"
        except ValueError:
            print("Invalid day! Using time only.")
            return f"{hour}:{minutes} {am_pm}"
        month = input("Select month (1-12, press x or Enter to cancel): ").strip()
        if month.lower() == "x" or month == "":
            return f"{hour}:{minutes} {am_pm}"
        try:
            month = int(month)
            if not 1 <= month <= 12:
                raise ValueError
            month = f"{month:02d}"
        except ValueError:
            print("Invalid month! Using time only.")
            return f"{hour}:{minutes} {am_pm}"
        year = input("Select year (e.g., 2025, press t for this year, x or Enter to cancel): ").strip()
        if year.lower() == "x" or year == "":
            return f"{hour}:{minutes} {am_pm}"
        if year.lower() == "t":
            year = str(datetime.now().year)
        else:
            try:
                year = int(year)
                if not 2000 <= year <= 2099:
                    raise ValueError
            except ValueError:
                print("Invalid year! Using time only.")
                return f"{hour}:{minutes} {am_pm}"
    if is_valid_datetime(hour, minutes, am_pm, day, month, year):
        return f"{hour}:{minutes} {am_pm} {day}-{month}-{year}"
    print("Invalid date/time! Skipping due date.")
    return ""

# Load tasks at startup
load_tasks()

# Main loop
while True:
    print("\nTo-Do App")
    print("1. Add task")
    print("2. Delete task")
    print("3. Edit task")
    print("4. View tasks")
    print("5. Exit")
    choice = input("Choose an option (1-5): ").strip()

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
            category = input("Enter category (Work/Personal, press Enter for Personal): ").strip()
            category_map = {"W": "Work", "P": "Personal"}
            category = category_map.get(category.upper(), "Personal") if category else "Personal"
            due_date = get_due_date()
            add_task(task, priority, due_date, category)
    elif choice == "2":
        view_tasks(pause=False, default_view=True)
        index = input("Enter task number to delete (press x to cancel): ").strip()
        if index.lower() == "x" or index == "":
            print("Task deletion canceled.")
        else:
            try:
                index = int(index)
                delete_task(index)
            except ValueError:
                print("Invalid input! Please enter a number or 'x'.")
    elif choice == "3":
        view_tasks(pause=False, default_view=True)
        index = input("Enter task number to edit (press x to cancel): ").strip()
        if index.lower() == "x" or index == "":
            print("Edit canceled.")
        else:
            try:
                index = int(index)
                edit_task(index)
            except ValueError:
                print("Invalid input! Please enter a number or 'x'.")
    elif choice == "4":
        view_tasks()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")