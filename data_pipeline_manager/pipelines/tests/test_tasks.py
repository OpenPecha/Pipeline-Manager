from pathlib import Path
from unittest import mock

import pytest
from celery.result import EagerResult
from ocr_pipelines.config import ImportConfig as OcrImportConfig

from data_pipeline_manager.pipelines.models import Task, TaskStatus
from data_pipeline_manager.pipelines.tasks import run_ocr_import_pipelines
from data_pipeline_manager.pipelines.tests.factories import TaskFactory

pytestmark = pytest.mark.django_db


@mock.patch("data_pipeline_manager.pipelines.tasks.ocr_import_pipeline", autospec=True)
def test_run_ocr_import_pipelines(mock_ocr_import_pipeline, settings):
    """Test run_ocr_import_pipelines."""
    # setup - data
    pecha_id = "I00001"
    bdrc_scan_id = "W30305"
    credentials = {"username": "user", "password": "password"}
    config = OcrImportConfig(
        ocr_engine="google_vision",
        model_type="bo-t-i0-handwrit",
        lang_hint="bo",
        credentials=credentials,
        images_path=Path("/tmp/images"),
        ocr_outputs_path=Path("/tmp/ocr_outputs"),
    )
    task = TaskFactory()
    settings.CELERY_TASK_ALWAYS_EAGER = True

    # setup - expectations
    mock_ocr_import_pipeline.return_value = pecha_id

    # exercise
    task_result = run_ocr_import_pipelines.delay(
        pipeline_task_id=task.id,
        bdrc_scan_id=bdrc_scan_id,
        config_dict=config.to_dict(),
    )

    # verify
    assert isinstance(task_result, EagerResult)
    kwargs = mock_ocr_import_pipeline.call_args.kwargs
    assert kwargs["bdrc_scan_id"] == bdrc_scan_id
    assert kwargs["config"].to_dict() == config.to_dict()
    assert kwargs["images_path"] == Path("/tmp/images")
    assert kwargs["ocr_outputs_path"] == Path("/tmp/ocr_output")

    completed_task = Task.objects.get(id=task.id)
    assert completed_task.result == pecha_id
    assert completed_task.status == TaskStatus.SUCCESS
