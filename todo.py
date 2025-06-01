# Simple To-Do List App
import os

# Initialize tasks list (each task is a dictionary with task and priority)
tasks = []

# Load tasks from file
def load_tasks():
    global tasks
    tasks = []
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    task, priority = line.rsplit(" | ", 1)
                    tasks.append({"task": task, "priority": priority})
        print("Tasks loaded from tasks.txt")

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(f"{task['task']} | {task['priority']}\n")
    print("Tasks saved to tasks.txt")

def add_task(task, priority):
    tasks.append({"task": task, "priority": priority})
    print(f"Added task: {task} (Priority: {priority})")
    save_tasks()

def view_tasks(pause=True):
    if not tasks:
        print("No tasks yet!")
    else:
        print("Your tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task['task']} (Priority: {task['priority']})")
    if pause:
        input("Press Enter to continue...")

def delete_task(index):
    try:
        task = tasks.pop(index - 1)
        print(f"Deleted task: {task['task']} (Priority: {task['priority']})")
        save_tasks()
    except IndexError:
        print("Invalid task number!")

# Load tasks at startup
load_tasks()

# Main loop
while True:
    print("\nTo-Do List App")
    print("1. Add task")
    print("2. View tasks")
    print("3. Delete task")
    print("4. Exit")
    choice = input("Choose an option (1-4): ")

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
            add_task(task, priority)
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