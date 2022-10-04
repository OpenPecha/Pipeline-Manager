import pytest
from django.test import RequestFactory

from data_pipeline_manager.pipelines import views

from .factories import BatchFactory, TaskFactory

pytestmark = pytest.mark.django_db


class TestDashboard:
    def test_ok(self, rf: RequestFactory):
        request = rf.get("/fake-url/")

        response = views.dashboard(request)

        assert response.status_code == 200


class TestBatchTaskListView:
    def test_ok(self, rf: RequestFactory):
        request = rf.get("/fake-url")

        response = views.batch_task_list_view(request)

        assert response.status_code == 200


class TestBatchDetailView:
    def test_ok(self, rf: RequestFactory):
        batch = BatchFactory()
        batch.run()
        request = rf.get("/fake-url")

        response = views.batch_task_detail_view(request, pk=batch.pk)

        assert response.status_code == 200


class TestTaskDetailView:
    def test_ok(self, rf: RequestFactory):
        task = TaskFactory()
        request = rf.get("/fake-url")

        response = views.task_detail_view(request, pk=task.pk)

        assert response.status_code == 200
