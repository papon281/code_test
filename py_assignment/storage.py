import json
import os
from task_manager import Task


class Storage:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**task) for task in tasks_data]
        else:
            # Create the tasks.json file if it doesn't exist
            with open(self.filename, 'w') as f:
                json.dump([], f)  # Initialize with an empty list

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump([task.__dict__ for task in self.tasks], f)

    def save_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def update_task(self, updated_task):
        for i, task in enumerate(self.tasks):
            if task.title == updated_task.title:
                self.tasks[i] = updated_task
                self.save_tasks()
                break

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def get_all_tasks(self):
        return list(self.tasks)

    def clear_all_tasks(self):
        self.tasks = []
        self.save_tasks()
