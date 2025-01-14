#!/usr/bin/env python3
import json
import sys
from datetime import datetime
import os
import cmd
import shlex

class Task:
    """Represents a single task"""
    def __init__(self, task_id, description, status='todo'):
        self.id = task_id
        self.description = description
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['id'], data['description'], data['status'])
        task.created_at = data['createdAt']
        task.updated_at = data['updatedAt']
        return task

class TaskManager:
    """Manages task operations and storage"""
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except json.JSONDecodeError:
            return []

    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            data = [task.to_dict() for task in self.tasks]
            json.dump(data, f, indent=2)

    def get_next_id(self):
        """Generate next task ID"""
        return max([task.id for task in self.tasks], default=0) + 1

    def add_task(self, description):
        """Add a new task"""
        task_id = self.get_next_id()
        task = Task(task_id, description)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task added successfully (ID: {task_id})")

    def update_task(self, task_id, new_description):
        """Update a task's description"""
        task_id = int(task_id)
        for task in self.tasks:
            if task.id == task_id:
                task.description = new_description
                task.updated_at = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task {task_id} updated successfully")
                return
        print(f"Task with ID {task_id} not found")

    def delete_task(self, task_id):
        """Delete a task"""
        task_id = int(task_id)
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        
        if len(self.tasks) < initial_length:
            self.save_tasks()
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task with ID {task_id} not found")

    def mark_task(self, task_id, status):
        """Mark a task with a specific status"""
        task_id = int(task_id)
        for task in self.tasks:
            if task.id == task_id:
                task.status = status
                task.updated_at = datetime.now().isoformat()
                self.save_tasks()
                print(f"Task {task_id} marked as {status}")
                return
        print(f"Task with ID {task_id} not found")

    def list_tasks(self, status=None):
        """List tasks, optionally filtered by status"""
        if not self.tasks:
            print("📝 No tasks found")
            return

        filtered_tasks = self.tasks
        if status:
            filtered_tasks = [task for task in self.tasks if task.status == status]

        if not filtered_tasks:
            print(f"📝 No tasks found with status: {status}")
            return

        status_emoji = {
            'todo': '📋',
            'in-progress': '🔄',
            'done': '✅'
        }

        print("\n📑 Task List:")
        print("─" * 50)
        print(f"{'ID':<4} {'Status':<15} Description")
        print("─" * 50)

        for task in filtered_tasks:
            emoji = status_emoji.get(task.status, '')
            print(f"{task.id:<4} {emoji} {task.status:<12} {task.description}")
        print("─" * 50)

class TaskShell(cmd.Cmd):
    """Interactive shell for task management"""
    intro = '''
    🗒️  Welcome to Task Manager! 🗒️
    Type 'help' to list commands.
    Type 'quit' to exit.
    '''
    prompt = '(task) '

    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()

    def do_add(self, arg):
        """Add a new task.
        Usage: add "task description" """
        if not arg:
            print("Error: Please provide a task description")
            return
        self.task_manager.add_task(arg)

    def do_update(self, arg):
        """Update a task description.
        Usage: update <id> "new description" """
        try:
            args = shlex.split(arg)
            if len(args) != 2:
                print("Error: Please provide task ID and new description")
                return
            self.task_manager.update_task(args[0], args[1])
        except ValueError:
            print("Error: Invalid arguments")

    def do_delete(self, arg):
        """Delete a task.
        Usage: delete <id>"""
        if not arg.isdigit():
            print("Error: Please provide a valid task ID")
            return
        self.task_manager.delete_task(arg)

    def do_progress(self, arg):
        """Mark a task as in-progress.
        Usage: progress <id>"""
        if not arg.isdigit():
            print("Error: Please provide a valid task ID")
            return
        self.task_manager.mark_task(arg, "in-progress")

    def do_done(self, arg):
        """Mark a task as done.
        Usage: done <id>"""
        if not arg.isdigit():
            print("Error: Please provide a valid task ID")
            return
        self.task_manager.mark_task(arg, "done")

    def do_list(self, arg):
        """List tasks, optionally filtered by status.
        Usage: list [done|todo|in-progress]"""
        if arg and arg not in ["done", "todo", "in-progress"]:
            print("Error: Invalid status filter")
            return
        self.task_manager.list_tasks(arg if arg else None)

    def do_quit(self, arg):
        """Exit the task manager"""
        print("\nGoodbye! 👋")
        return True

    def do_EOF(self, arg):
        """Exit on Ctrl-D"""
        print()
        return self.do_quit(arg)

    # Shortcuts for common commands
    do_q = do_quit
    do_exit = do_quit

def print_usage():
    print("""
Usage:
    task.py add "task description"
    task.py update <id> "new description"
    task.py delete <id>
    task.py mark-in-progress <id>
    task.py mark-done <id>
    task.py list [done|todo|in-progress]
    """)

def main():
    task_manager = TaskManager()
    
    if len(sys.argv) > 1:
        # Command-line mode
        command = sys.argv[1]
        try:
            if command == "add" and len(sys.argv) == 3:
                task_manager.add_task(sys.argv[2])
            elif command == "update" and len(sys.argv) == 4:
                task_manager.update_task(sys.argv[2], sys.argv[3])
            elif command == "delete" and len(sys.argv) == 3:
                task_manager.delete_task(sys.argv[2])
            elif command == "mark-in-progress" and len(sys.argv) == 3:
                task_manager.mark_task(sys.argv[2], "in-progress")
            elif command == "mark-done" and len(sys.argv) == 3:
                task_manager.mark_task(sys.argv[2], "done")
            elif command == "list":
                if len(sys.argv) == 2:
                    task_manager.list_tasks()
                elif len(sys.argv) == 3 and sys.argv[2] in ["done", "todo", "in-progress"]:
                    task_manager.list_tasks(sys.argv[2])
                else:
                    print_usage()
            else:
                print_usage()
        except ValueError as e:
            print(f"Error: Invalid task ID. Please provide a valid number.")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        # Interactive mode
        TaskShell().cmdloop()

if __name__ == "__main__":
    main()
