import time
from datetime import datetime

from config import celery_app
from data_pipeline_manager.pipelines.models import Task


@celery_app.task()
def run_ocr_import_pipelines(pipeline_task_id, *args, **kwargs):
    """Run OCR import pipelines."""
    time.sleep(20)
    task = Task.objects.get(id=pipeline_task_id)
    task.status = Task.TaskStatus.COMPLETED
    task.completed_on = datetime.now()
    task.result = "I000001"
    task.save()
