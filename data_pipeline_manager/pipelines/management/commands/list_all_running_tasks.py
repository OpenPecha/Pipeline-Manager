from django.core.management.base import BaseCommand

from config import celery_app


class Command(BaseCommand):
    help = "List running Celery tasks"

    def handle(self, *args, **options):
        # Use the Celery inspect API to get a list of running tasks
        i = celery_app.control.inspect()
        active_tasks = i.active()
        if active_tasks is not None:
            for worker, tasks in active_tasks.items():
                for task in tasks:
                    self.stdout.write(
                        f'Task {task["id"]} is running on worker {worker}'
                    )
