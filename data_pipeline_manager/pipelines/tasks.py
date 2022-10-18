import traceback
from datetime import datetime
from pathlib import Path

from ocr_pipelines.config import ImportConfig
from ocr_pipelines.pipelines import import_pipeline as ocr_import_pipeline

from config import celery_app
from data_pipeline_manager.pipelines.models import Task, TaskStatus


class OCRImportConfig(ImportConfig):
    def to_dict(self):
        return {
            "ocr_engine": self.ocr_engine,
            "model_type": self.model_type,
            "language": self.lang_hint,
        }

    @classmethod
    def parse_obj(cls, obj):
        """Parse a dict into a config object"""
        return cls(
            ocr_engine=obj["ocr_engine"],
            model_type=obj["model_type"],
            lang_hint=obj["language"],
        )


@celery_app.task()
def run_ocr_import_pipelines(
    pipeline_task_id, work_id, config_dict, images_dir, ocr_output_dir
):
    """Run OCR import pipelines."""
    try:
        config = OCRImportConfig.parse_obj(config_dict)
        pecha_id = ocr_import_pipeline(
            work_id=work_id,
            config=config,
            img_download_dir=Path(images_dir),
            ocr_base_dir=Path(ocr_output_dir),
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
