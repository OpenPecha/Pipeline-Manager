import pytest
from celery.result import EagerResult

from data_pipeline_manager.pipelines.models import Task, TaskStatus
from data_pipeline_manager.pipelines.tasks import run_ocr_import_pipelines

from .factories import TaskFactory

pytestmark = pytest.mark.django_db


def test_run_ocr_import_pipelines(settings):
    """Test run_ocr_import_pipelines."""
    task = TaskFactory()
    settings.CELERY_TASK_ALWAYS_EAGER = True

    task_result = run_ocr_import_pipelines.delay(task.id)

    completed_task = Task.objects.get(id=task.id)

    assert isinstance(task_result, EagerResult)
    assert completed_task.result == "I000001"
    assert completed_task.status == TaskStatus.SUCCESS
