# Simple To-Do List App
import os

# Initialize tasks list
tasks = []

# Load tasks from file (if exists)
def load_tasks():
    global tasks
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            tasks = [line.strip() for line in file if line.strip()]
            print("Tasks loaded from tasks.txt")

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")
    print("Tasks saved to tasks.txt")

def add_task(task):
    tasks.append(task)
    print(f"Added task: {task}")
    save_tasks()

def view_tasks():
    if not tasks:
        print("No tasks yet!")
    else:
        print("Your tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def delete_task(index):
    try:
        task = tasks.pop(index - 1)
        print(f"Deleted task: {task}")
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
        task = input("Enter task (or type 'cancel' to return to menu): ").strip()
        if task.lower() == "cancel" or task == "":
            print("Task addition canceled.")
        else:
            add_task(task)
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        view_tasks()
        index = int(input("Enter task number to delete: "))
        delete_task(index)
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")