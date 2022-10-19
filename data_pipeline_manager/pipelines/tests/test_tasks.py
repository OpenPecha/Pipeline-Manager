from pathlib import Path
from unittest import mock

import pytest
from celery.result import EagerResult

from data_pipeline_manager.pipelines.models import Task, TaskStatus
from data_pipeline_manager.pipelines.tasks import (
    OCRImportConfig,
    run_ocr_import_pipelines,
)

from .factories import TaskFactory

pytestmark = pytest.mark.django_db


@mock.patch("data_pipeline_manager.pipelines.tasks.ocr_import_pipeline", autospec=True)
def test_run_ocr_import_pipelines(mock_ocr_import_pipeline, settings):
    """Test run_ocr_import_pipelines."""
    # setup - data
    pecha_id = "I00001"
    work_id = "W30305"
    config = OCRImportConfig(
        ocr_engine="google_vision", model_type="bo-t-i0-handwrit", lang_hint="bo"
    )
    task = TaskFactory()
    settings.CELERY_TASK_ALWAYS_EAGER = True

    # setup - expectations
    mock_ocr_import_pipeline.return_value = pecha_id

    # exercise
    task_result = run_ocr_import_pipelines.delay(
        pipeline_task_id=task.id,
        work_id=work_id,
        config_dict=config.to_dict(),
        images_dir="/tmp/images",
        ocr_output_dir="/tmp/ocr_output",
    )

    # verify
    assert isinstance(task_result, EagerResult)
    kwargs = mock_ocr_import_pipeline.call_args.kwargs
    assert kwargs["work_id"] == work_id
    assert kwargs["config"].to_dict() == config.to_dict()
    assert kwargs["img_download_dir"] == Path("/tmp/images")
    assert kwargs["ocr_base_dir"] == Path("/tmp/ocr_output")

    completed_task = Task.objects.get(id=task.id)
    assert completed_task.result == pecha_id
    assert completed_task.status == TaskStatus.SUCCESS
