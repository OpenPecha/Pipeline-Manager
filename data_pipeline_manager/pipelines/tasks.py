from datetime import datetime

from config import celery_app
from data_pipeline_manager.pipelines.models import Task, TaskStatus


@celery_app.task()
def run_ocr_import_pipelines(pipeline_task_id, ocr_task_func):
    """Run OCR import pipelines."""
    try:
        pecha_id = ocr_task_func()
    except Exception as e:
        Task.objects.filter(id=pipeline_task_id).update(
            status=TaskStatus.FAILED, error=e
        )
        raise e
    task = Task.objects.get(id=pipeline_task_id)
    task.status = TaskStatus.SUCCESS
    task.completed_on = datetime.now()
    task.result = pecha_id
    task.save()
