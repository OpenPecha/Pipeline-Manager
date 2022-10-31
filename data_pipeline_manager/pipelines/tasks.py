import traceback
from datetime import datetime

from ocr_pipelines.config import ImportConfig as OcrImportConfig
from ocr_pipelines.pipelines import import_pipeline as ocr_import_pipeline

from config import celery_app
from data_pipeline_manager.pipelines.models import Task, TaskStatus


@celery_app.task()
def run_ocr_import_pipelines(pipeline_task_id, bdrc_scan_id, config_dict):
    """Run OCR import pipelines."""
    try:
        config = OcrImportConfig.from_dict(config_dict)
        pecha_id = ocr_import_pipeline(
            bdrc_scan_id=bdrc_scan_id,
            config=config,
        )
    except Exception:
        error_trackback = traceback.format_exc()
        Task.objects.filter(id=pipeline_task_id).update(
            status=TaskStatus.FAILURE, error=error_trackback
        )
        return
    task = Task.objects.get(id=pipeline_task_id)
    task.status = TaskStatus.SUCCESS
    task.completed_on = datetime.now()
    task.result = pecha_id
    task.save()
