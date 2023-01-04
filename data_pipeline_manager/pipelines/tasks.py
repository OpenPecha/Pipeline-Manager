import traceback
from datetime import datetime

import requests
from django.utils import timezone
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
        result = ocr_import_pipeline(
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
    task.completed_on = timezone.now()
    task.result = result
    task.save()


def get_repos(page: int) -> list:
    """Get the OpenPecha-Data repos of a `page`."""
    url = f"https://api.github.com/orgs/OpenPecha-Data/repos?sort=created&page={page}"
    response = requests.get(url)
    return response.json()


def get_repo_created_datetime(repo: dict) -> datetime:
    """Get the created datetime of a repo in UTC."""
    d = datetime.fromisoformat(repo["created_at"][:-1])
    return d.replace(tzinfo=timezone.utc)


def get_pecha_id_from_bdrc_scan_id(bdrc_scan_id: str, task_started: datetime) -> str:
    """Get the pecha id from a BDRC scan id."""
    created_datetime_of_first_repo_of_the_page = None
    page = 1
    while True:
        repos = get_repos(page)
        created_datetime_of_first_repo_of_the_page = get_repo_created_datetime(repos[0])
        if created_datetime_of_first_repo_of_the_page < task_started:
            return None, None
        for repo in repos:
            repo_desc = repo["description"]
            if repo_desc and bdrc_scan_id in repo_desc:
                return repo["name"], get_repo_created_datetime(repo)
        page += 1


def get_pecha_result(pecha_id: str) -> dict:
    return {
        "pecha_id": pecha_id,
        "pecha_url": f"https://github.com/OpenPecha-Data/{pecha_id}",
    }


@celery_app.task()
def handle_broken_tasks():
    """Handle a broken tasks."""
    running_tasks = Task.objects.filter(status=TaskStatus.RUNNING)
    for task in running_tasks:
        pecha_id, pecha_created_datetime = get_pecha_id_from_bdrc_scan_id(
            task.input, task.started_on
        )
        if not pecha_id:
            continue

        task.status = TaskStatus.SUCCESS
        task.completed_on = pecha_created_datetime
        task.result = get_pecha_result(pecha_id)
        task.save()
