# Simple To-Do App
import os
from datetime import datetime, timedelta

# Initialize tasks and categories lists
tasks = []
categories = []

# Load categories from file
def load_categories():
    global categories
    categories = []
    if os.path.exists("categories.txt"):
        with open("categories.txt", "r") as f:
            for line in f:
                category = line.strip()
                if category and category not in categories:
                    categories.append(category)
    if not categories:
        categories = ["Work", "Personal"]  # Default categories
    save_categories()

# Save categories to file
def save_categories():
    with open("categories.txt", "w") as f:
        for category in categories:
            f.write(f"{category}\n")

# Load tasks from file
def load_tasks():
    global tasks
    tasks = []
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.rsplit(" | ", 5)
                    task = parts[0]
                    priority = parts[1] if len(parts) > 1 else "Medium"
                    due_date = parts[2] if len(parts) > 2 else ""
                    category = parts[3] if len(parts) > 3 else categories[0]
                    completed = parts[4].lower() == "true" if len(parts) > 4 else False
                    recurrence = parts[5] if len(parts) > 5 else "None"
                    # Ensure category and recurrence are valid
                    if category not in categories:
                        category = categories[0]
                    valid_recurrences = ["None", "Daily", "Weekly", "Monthly", "Yearly"]
                    if recurrence not in valid_recurrences:
                        recurrence = "None"
                    tasks.append({"task": task, "priority": priority, "due_date": due_date, "category": category, "completed": completed, "recurrence": recurrence})
        save_tasks()  # Update file format
    print("Tasks loaded from tasks.txt")

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            due_date = task["due_date"] if task["due_date"] else ""
            f.write(f"{task['task']} | {task['priority']} | {due_date} | {task['category']} | {task['completed']} | {task['recurrence']}\n")

# Validate date/time components
def is_valid_datetime(hour, minutes, am_pm, day, month, year):
    if not all([hour, minutes, am_pm, day, month, year]):
        return True  # Allow partial or empty input
    try:
        datetime.strptime(f"{hour}:{minutes} {am_pm} {day}-{month}-{year}", "%I:%M %p %d-%m-%Y")
        return True
    except ValueError:
        return False

def add_task(task, priority, due_date, category, recurrence):
    tasks.append({"task": task, "priority": priority, "due_date": due_date, "category": category, "completed": False, "recurrence": recurrence})
    due_date_display = f", Due: {due_date}" if due_date else ""
    category_display = f", Category: {category}"
    recurrence_display = f", Recurring: {recurrence}" if recurrence != "None" else ""
    print(f"Added task: {task} (Priority: {priority}{due_date_display}{category_display}{recurrence_display})")
    save_tasks()

def view_tasks(tasks_to_view, sort_method="priority", pause=True):
    if not tasks_to_view:
        print("No tasks match the filter!")
        if pause:
            input("Press Enter to continue...")
        return
    priority_order = {"High": 2, "Medium": 1, "Low": 0}
    def get_due_date(task):
        if not task["due_date"]:
            return datetime.max  # No due date goes last
        try:
            return datetime.strptime(task["due_date"], "%I:%M %p %d-%m-%Y")
        except ValueError:
            return datetime.max  # Invalid or time-only due date goes last
    if sort_method == "priority":
        tasks_to_view = sorted(tasks_to_view, key=lambda x: priority_order[x["priority"]], reverse=True)
    elif sort_method == "due date":
        tasks_to_view = sorted(tasks_to_view, key=get_due_date)
    elif sort_method == "category":
        tasks_to_view = sorted(tasks_to_view, key=lambda x: x["category"])
    print(f"Tasks sorted by {sort_method}")
    print("Your tasks:")
    for i, task in enumerate(tasks_to_view, 1):
        due_date_display = f"Due: {task['due_date']}" if task['due_date'] else ""
        priority_display = f"Priority: {task['priority']}"
        category_display = f"Category: {task['category']}"
        recurrence_display = f"Recurring: {task['recurrence']}" if task["recurrence"] != "None" else ""
        completed_display = "[X]" if task["completed"] else "[ ]"
        if sort_method == "due date" and task["due_date"]:
            display = f"{category_display}, {due_date_display}, {priority_display}, {recurrence_display}"
        else:
            display = f"{category_display}, {priority_display}{', ' + due_date_display if task['due_date'] else ''}{', ' + recurrence_display if recurrence_display else ''}"
        print(f"{i}. {completed_display} {task['task']} ({display})")
    if pause:
        input("Press Enter to continue...")

def delete_task(index):
    try:
        task = tasks.pop(index - 1)
        due_date_display = f", Due: {task['due_date']}" if task['due_date'] else ""
        category_display = f", Category: {task['category']}"
        recurrence_display = f", Recurring: {task['recurrence']}" if task["recurrence"] != "None" else ""
        completed_display = "[X]" if task["completed"] else "[ ]"
        print(f"Deleted task: {completed_display} {task['task']} (Priority: {task['priority']}{due_date_display}{category_display}{recurrence_display})")
        save_tasks()
    except IndexError:
        print("Invalid task number!")

def edit_task(index):
    try:
        task = tasks[index - 1]
        due_date_display = f", Due: {task['due_date']}" if task['due_date'] else ""
        category_display = f", Category: {task['category']}"
        recurrence_display = f", Recurring: {task['recurrence']}" if task["recurrence"] != "None" else ""
        completed_display = "[X]" if task["completed"] else "[ ]"
        print(f"Editing task: {completed_display} {task['task']} (Priority: {task['priority']}{due_date_display}{category_display}{recurrence_display})")
        choice = input("Edit: 1. Description 2. Priority 3. Due date 4. Category 5. Recurrence (press x to cancel): ").strip()
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
            if not categories:
                print("No categories available! Add categories first.")
                return
            print("Available categories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            category_input = input("Enter category number or new category name (press Enter for first category): ").strip()
            if category_input.lower() == "x":
                print("Edit canceled.")
                return
            if not category_input:
                category = categories[0]
            else:
                try:
                    category_index = int(category_input) - 1
                    if 0 <= category_index < len(categories):
                        category = categories[category_index]
                    else:
                        print("Invalid category number! Keeping original.")
                        return
                except ValueError:
                    if category_input and category_input not in categories:
                        categories.append(category_input)
                        save_categories()
                    category = category_input
            tasks[index - 1]["category"] = category
            print(f"Updated category to: Category: {category}")
        elif choice == "5":
            recurrence = input("Enter recurrence (D=Daily, W=Weekly, M=Monthly, Y=Yearly, press Enter for None): ").strip().upper()
            recurrence_map = {"D": "Daily", "W": "Weekly", "M": "Monthly", "Y": "Yearly"}
            if recurrence.lower() == "x":
                print("Edit canceled.")
                return
            if not recurrence:
                recurrence = "None"
            else:
                recurrence = recurrence_map.get(recurrence, "None")
                if recurrence == "None":
                    print("Invalid recurrence! Setting to None.")
            tasks[index - 1]["recurrence"] = recurrence
            print(f"Updated recurrence to: Recurring: {recurrence}")
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

def manage_categories():
    while True:
        print("\nManage Categories")
        print("1. Add category")
        print("2. Remove category")
        print("3. List categories")
        print("4. Back")
        choice = input("Choose an option (1-4, press x to cancel): ").strip()
        if choice.lower() == "x" or choice == "4":
            print("Exiting category management.")
            break
        if choice == "1":
            category = input("Enter new category name (press x to cancel): ").strip()
            if category.lower() == "x" or not category:
                print("Category addition canceled.")
                continue
            if category in categories:
                print("Category already exists!")
                continue
            categories.append(category)
            save_categories()
            print(f"Added category: {category}")
        elif choice == "2":
            if not categories:
                print("No categories to remove!")
                continue
            print("Available categories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            index = input("Enter category number to remove (press x to cancel): ").strip()
            if index.lower() == "x" or not index:
                print("Category removal canceled.")
                continue
            try:
                index = int(index) - 1
                if 0 <= index < len(categories):
                    category = categories[index]
                    if any(task["category"] == category for task in tasks):
                        print(f"Cannot remove '{category}' because tasks are still assigned to it. Please reassign or delete those tasks first.")
                        continue
                    categories.pop(index)
                    save_categories()
                    print(f"Removed category: {category}")
                else:
                    print("Invalid category number!")
            except ValueError:
                print("Invalid input! Please enter a number or 'x'.")
        elif choice == "3":
            if not categories:
                print("No categories available!")
            else:
                print("Available categories:")
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
            input("Press Enter to continue...")
        else:
            print("Invalid choice!")

def mark_task(index):
    try:
        task = tasks[index - 1]
        task["completed"] = not task["completed"]
        status = "completed" if task["completed"] else "uncompleted"
        due_date_display = f", Due: {task['due_date']}" if task['due_date'] else ""
        category_display = f", Category: {task['category']}"
        recurrence_display = f", Recurring: {task['recurrence']}" if task["recurrence"] != "None" else ""
        completed_display = "[X]" if task["completed"] else "[ ]"
        print(f"Marked task as {status}: {completed_display} {task['task']} (Priority: {task['priority']}{due_date_display}{category_display}{recurrence_display})")
        if task["completed"] and task["recurrence"] != "None" and task["due_date"]:
            recurrence_map = {
                "Daily": timedelta(days=1),
                "Weekly": timedelta(weeks=1),
                "Monthly": timedelta(days=30),  # Approximate
                "Yearly": timedelta(days=365)
            }
            try:
                due_date = datetime.strptime(task["due_date"], "%I:%M %p %d-%m-%Y")
                new_due_date = due_date + recurrence_map[task["recurrence"]]
                new_due_date_str = new_due_date.strftime("%I:%M %p %d-%m-%Y")
                tasks.append({
                    "task": task["task"],
                    "priority": task["priority"],
                    "due_date": new_due_date_str,
                    "category": task["category"],
                    "completed": False,
                    "recurrence": task["recurrence"]
                })
                print(f"Created new recurring task: {task['task']} (Due: {new_due_date_str})")
            except ValueError:
                print("Invalid due date format; new recurring task not created.")
        save_tasks()
    except IndexError:
        print("Invalid task number!")

def filter_tasks():
    choice = input("Filter by: 1. All tasks 2. Incomplete tasks 3. Completed tasks 4. By category 5. By recurrence (press x to cancel): ").strip()
    if choice.lower() == "x" or choice == "":
        print("Filter canceled.")
        return
    tasks_to_view = tasks
    filter_method = "all tasks"
    if choice == "2":
        tasks_to_view = [task for task in tasks if not task["completed"]]
        filter_method = "incomplete tasks"
    elif choice == "3":
        tasks_to_view = [task for task in tasks if task["completed"]]
        filter_method = "completed tasks"
    elif choice == "4":
        if not categories:
            print("No categories available!")
            input("Press Enter to continue...")
            return
        print("Available categories:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        category_input = input("Enter category number (press x to cancel): ").strip()
        if category_input.lower() == "x" or not category_input:
            print("Filter canceled.")
            return
        try:
            category_index = int(category_input) - 1
            if 0 <= category_index < len(categories):
                selected_category = categories[category_index]
                tasks_to_view = [task for task in tasks if task["category"] == selected_category]
                filter_method = f"category '{selected_category}'"
            else:
                print("Invalid category number!")
                return
        except ValueError:
            print("Invalid input! Please enter a number or 'x'.")
    elif choice == "5":
        print("Recurrence types:")
        recurrence_types = ["None", "Daily", "Weekly", "Monthly", "Yearly"]
        for i, rec in enumerate(recurrence_types, 1):
            print(f"{i}. {rec}")
        recurrence_input = input("Enter recurrence number (press x to cancel): ").strip()
        if recurrence_input.lower() == "x" or not recurrence_input:
            print("Filter canceled.")
            return
        try:
            recurrence_index = int(recurrence_input) - 1
            if 0 <= recurrence_index < len(recurrence_types):
                selected_recurrence = recurrence_types[recurrence_index]
                tasks_to_view = [task for task in tasks if task["recurrence"] == selected_recurrence]
                filter_method = f"recurrence '{selected_recurrence}'"
            else:
                print("Invalid recurrence number!")
                return
        except ValueError:
            print("Invalid input! Please enter a number or 'x'.")
    elif choice != "1":
        print("Invalid choice!")
        return
    print(f"Filtering by: {filter_method}")
    sort_choice = input("Sort by: 1. Priority (High > Medium > Low) 2. Due date 3. Category (press Enter for priority): ").strip()
    sort_method = "priority"
    if sort_choice == "2":
        sort_method = "due date"
    elif sort_choice == "3":
        sort_method = "category"
    view_tasks(tasks_to_view, sort_method)

# Load categories and tasks at startup
load_categories()
load_tasks()

# Main loop
while True:
    print("\nTo-Do App")
    print("1. Add task")
    print("2. Delete task")
    print("3. Edit task")
    print("4. Manage categories")
    print("5. Mark task as completed/uncompleted")
    print("6. View tasks")
    print("7. Filter tasks")
    print("8. Exit")
    choice = input("Choose an option (1-8): ").strip()

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
            if not categories:
                print("No categories available! Add categories first.")
                continue
            print("Available categories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            category_input = input("Enter category number or new category name (press Enter for first category): ").strip()
            if category_input.lower() == "x":
                print("Task addition canceled.")
                continue
            if not category_input:
                category = categories[0]
            else:
                try:
                    category_index = int(category_input) - 1
                    if 0 <= category_index < len(categories):
                        category = categories[category_index]
                    else:
                        print("Invalid category number! Using first category.")
                        category = categories[0]
                except ValueError:
                    if category_input and category_input not in categories:
                        categories.append(category_input)
                        save_categories()
                    category = category_input
            due_date = get_due_date()
            recurrence = input("Enter recurrence (D=Daily, W=Weekly, M=Monthly, Y=Yearly, press Enter for None): ").strip().upper()
            recurrence_map = {"D": "Daily", "W": "Weekly", "M": "Monthly", "Y": "Yearly"}
            if recurrence.lower() == "x":
                print("Task addition canceled.")
                continue
            if not recurrence:
                recurrence = "None"
            else:
                recurrence = recurrence_map.get(recurrence, "None")
                if recurrence == "None":
                    print("Invalid recurrence! Defaulting to None.")
            add_task(task, priority, due_date, category, recurrence)
    elif choice == "2":
        view_tasks(tasks, "priority", pause=False)
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
        view_tasks(tasks, "priority", pause=False)
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
        manage_categories()
    elif choice == "5":
        view_tasks(tasks, "priority", pause=False)
        index = input("Enter task number to mark as completed/uncompleted (press x to cancel): ").strip()
        if index.lower() == "x" or index == "":
            print("Marking canceled.")
        else:
            try:
                index = int(index)
                mark_task(index)
            except ValueError:
                print("Invalid input! Please enter a number or 'x'.")
    elif choice == "6":
        view_tasks(tasks)
    elif choice == "7":
        filter_tasks()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")