# Simple To-Do List App
tasks = []

def add_task(task):
    tasks.append(task)
    print(f"Added task: {task}")

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
    except IndexError:
        print("Invalid task number!")

# Main loop
while True:
    print("\nTo-Do List App")
    print("1. Add task")
    print("2. View tasks")
    print("3. Delete task")
    print("4. Exit")
    choice = input("Choose an option (1-4): ")

    if choice == "1":
        task = input("Enter task: ")
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