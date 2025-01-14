import json
import os

def load_tasks(filename):
    """Load tasks from a JSON file."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_tasks(filename, tasks):
    """Save tasks to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(tasks, file, indent=2)

def get_next_id(tasks):
    """Generate the next task ID."""
    return max((task['id'] for task in tasks), default=0) + 1

def add_task(tasks, description):
    """Add a new task."""
    task = {
        'id': get_next_id(tasks),
        'description': description,
        'status': 'todo'
    }
    tasks.append(task)
    print(f"Task added: {task['id']} - {description}")

def update_task(tasks, task_id, new_description):
    """Update the description of an existing task."""
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            print(f"Task {task_id} updated.")
            return
    print(f"Task {task_id} not found.")

def delete_task(tasks, task_id):
    """Delete a task by ID."""
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            print(f"Task {task_id} deleted.")
            return
    print(f"Task {task_id} not found.")

def mark_task(tasks, task_id, status):
    """Mark a task as done or in-progress."""
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            print(f"Task {task_id} marked as {status}.")
            return
    print(f"Task {task_id} not found.")

def list_tasks(tasks, status=None):
    """List all tasks, optionally filtered by status."""
    filtered_tasks = [task for task in tasks if not status or task['status'] == status]
    if not filtered_tasks:
        print("No tasks found.")
        return

    print("\nTasks:")
    print("ID  | Status       | Description")
    print("----|--------------|----------------")
    for task in filtered_tasks:
        print(f"{task['id']: <4}| {task['status']: <12} | {task['description']}")

def main():
    """Main function to run the task manager."""
    filename = "tasks.json"
    tasks = load_tasks(filename)

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. Mark Task")
        print("5. List Tasks")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            description = input("Enter task description: ")
            add_task(tasks, description)
        elif choice == "2":
            task_id = int(input("Enter task ID to update: "))
            new_description = input("Enter new description: ")
            update_task(tasks, task_id, new_description)
        elif choice == "3":
            task_id = int(input("Enter task ID to delete: "))
            delete_task(tasks, task_id)
        elif choice == "4":
            task_id = int(input("Enter task ID to mark: "))
            status = input("Enter status (todo, in-progress, done): ")
            mark_task(tasks, task_id, status)
        elif choice == "5":
            status = input("Enter status to filter (leave blank for all): ")
            list_tasks(tasks, status)
        elif choice == "6":
            save_tasks(filename, tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
