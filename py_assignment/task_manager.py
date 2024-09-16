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
        task = Task(title, description)
        self.storage.save_task(task)
        return task

    def complete_task(self, title):
        task = self.storage.get_task(title)
        if task:
            task.complete()
            self.storage.update_task(task)
            return True
        return False

    def list_tasks(self, include_completed=False):
        tasks = self.storage.get_all_tasks()
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]
        return tasks

    def generate_report(self):
        tasks = self.storage.get_all_tasks()
        total_tasks = len(tasks)
        completed_tasks = [task for task in tasks if task.completed]
        completed_count = len(completed_tasks)
        pending_count = total_tasks - completed_count

        # Calculate average time to complete a task
        total_time = 0
        for task in completed_tasks:
            created_time = datetime.fromisoformat(task.created_at)
            if task.completed_at:
                completed_time = datetime.fromisoformat(task.completed_at)
                total_time += (completed_time - created_time).total_seconds()

        average_time = total_time / completed_count if completed_count > 0 else 0  # Average in seconds

        report = {
            "total": total_tasks,
            "completed": completed_count,
            "pending": pending_count,
            "average_time": average_time
        }

        return report