#!/usr/bin/env python3
import json
import sys
from datetime import datetime
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file. Create file if it doesn't exist."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def get_next_id(tasks):
    """Generate next task ID."""
    return max([task['id'] for task in tasks], default=0) + 1

def add_task(description):
    """Add a new task."""
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    current_time = datetime.now().isoformat()
    
    new_task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': current_time,
        'updatedAt': current_time
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def update_task(task_id, new_description):
    """Update a task's description."""
    tasks = load_tasks()
    task_id = int(task_id)
    
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    
    print(f"Task with ID {task_id} not found")

def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    task_id = int(task_id)
    
    initial_length = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) < initial_length:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"Task with ID {task_id} not found")

def mark_task(task_id, status):
    """Mark a task as in-progress or done."""
    tasks = load_tasks()
    task_id = int(task_id)
    
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return
    
    print(f"Task with ID {task_id} not found")

def list_tasks(status=None):
    """List tasks, optionally filtered by status."""
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks found")
        return
        
    filtered_tasks = tasks
    if status:
        filtered_tasks = [task for task in tasks if task['status'] == status]
        
    if not filtered_tasks:
        print(f"No tasks found with status: {status}")
        return
        
    print("\nID  Status       Description")
    print("-" * 40)
    for task in filtered_tasks:
        print(f"{task['id']:<3} {task['status']:<12} {task['description']}")

def print_usage():
    """Print usage instructions."""
    print("""
Usage:
    task-cli add "task description"
    task-cli update <id> "new description"
    task-cli delete <id>
    task-cli mark-in-progress <id>
    task-cli mark-done <id>
    task-cli list
    task-cli list done
    task-cli list todo
    task-cli list in-progress
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    try:
        if command == "add" and len(sys.argv) == 3:
            add_task(sys.argv[2])
            
        elif command == "update" and len(sys.argv) == 4:
            update_task(sys.argv[2], sys.argv[3])
            
        elif command == "delete" and len(sys.argv) == 3:
            delete_task(sys.argv[2])
            
        elif command == "mark-in-progress" and len(sys.argv) == 3:
            mark_task(sys.argv[2], "in-progress")
            
        elif command == "mark-done" and len(sys.argv) == 3:
            mark_task(sys.argv[2], "done")
            
        elif command == "list":
            if len(sys.argv) == 2:
                list_tasks()
            elif len(sys.argv) == 3 and sys.argv[2] in ["done", "todo", "in-progress"]:
                list_tasks(sys.argv[2])
            else:
                print_usage()
                
        else:
            print_usage()
            
    except ValueError as e:
        print(f"Error: Invalid task ID. Please provide a valid number.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

