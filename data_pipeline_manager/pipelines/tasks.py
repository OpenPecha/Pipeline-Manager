import traceback
from datetime import datetime

from ocr_pipelines.config import ImportConfig as OcrImportConfig
from ocr_pipelines.metadata import Metadata
from ocr_pipelines.pipelines import import_pipeline as ocr_import_pipeline

from config import celery_app
from data_pipeline_manager.pipelines.models import Task, TaskStatus


class OcrMetadata(Metadata):
    @classmethod
    def from_dict(cls, metadata_dict: dict) -> "OcrMetadata":
        """Deserialize the metadata from a dictionary."""
        metadata_dict = metadata_dict.copy()
        metadata_dict["pipeline_config"] = OcrImportConfig(
            ocr_engine=metadata_dict["ocr_engine"],
            model_type=metadata_dict["ocr_model_type"],
            lang_hint=metadata_dict["ocr_lang_hint"],
        )
        del metadata_dict["ocr_engine"]
        del metadata_dict["ocr_model_type"]
        del metadata_dict["ocr_lang_hint"]
        return cls(**metadata_dict)


@celery_app.task()
def run_ocr_import_pipelines(
    pipeline_task_id: str, bdrc_scan_id: str, config_dict: dict, metadata_dict: dict
):
    """Run OCR import pipelines."""
    try:
        config = OcrImportConfig.from_dict(config_dict)
        metadata = OcrMetadata.from_dict(metadata_dict)
        pecha_id = ocr_import_pipeline(
            bdrc_scan_id=bdrc_scan_id,
            config=config,
            metadata=metadata,
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
