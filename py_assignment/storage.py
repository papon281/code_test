import json
import os
from task_manager import Task


class Storage:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = {}
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = {task['title']: Task(**task) for task in tasks_data}  # Use title as key
        else:
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.__dict__ for task in self.tasks.values()], f)

    def save_task(self, task):
        self.tasks[task.title] = task  # Use title as key
        self.save_tasks()

    def update_task(self, updated_task):
        self.tasks[updated_task.title] = updated_task  # Use title as key
        self.save_tasks()

    def get_task(self, title):
        return self.tasks.get(title)

    def get_all_tasks(self):
        return self.tasks  # Return the entire dictionary

    def clear_all_tasks(self):
        self.tasks = {}
        self.save_tasks()
