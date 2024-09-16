from datetime import datetime


class Task:

    def __init__(self, title, description, completed=False, created_at=None, completed_at=None):
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = created_at if created_at else datetime.now().isoformat()
        self.completed_at = completed_at

    def complete(self):
        self.completed = True
        self.completed_at = datetime.now().isoformat()


class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title, description):
        if title in self.storage.tasks:
            print("Task with title already exists. Please use a different title.")
            return  # Stop further execution if the task exists

        task = Task(title, description)
        self.storage.save_task(task)
        return task

    def complete_task(self, title):
        task = self.storage.get_task(title)
        if task:
            task.complete()  # Assuming complete() method updates the completed_at field
            self.storage.update_task(task)
            return True
        return False

    def list_tasks(self, include_completed=False):
        if include_completed:
            return list(self.storage.get_all_tasks().values())
        else:
            return [task for task in self.storage.get_all_tasks().values() if not task.completed]

    def generate_report(self):
        tasks = self.storage.get_all_tasks()
        total_tasks = len(tasks)
        completed_tasks = [task for task in tasks.values() if task.completed]
        completed_count = len(completed_tasks)
        pending_count = total_tasks - completed_count

        total_time = 0
        for task in completed_tasks:
            created_time = datetime.fromisoformat(task.created_at)
            completed_time = datetime.fromisoformat(task.completed_at) if task.completed_at else datetime.now()
            total_time += (completed_time - created_time).total_seconds()

        average_time = total_time / completed_count if completed_count > 0 else 0

        report = {
            "total": total_tasks,
            "completed": completed_count,
            "pending": pending_count,
            "average_time": average_time
        }

        return report
