import pytest
from django.test import RequestFactory

from data_pipeline_manager.pipelines.views import batch_task_list_view, dashboard

pytestmark = pytest.mark.django_db


class TestDashboard:
    def test_ok(self, rf: RequestFactory):
        request = rf.get("/fake-url/")

        response = dashboard(request)

        assert response.status_code == 200


class TestBatchTaskListView:
    def test_ok(self, rf: RequestFactory):
        request = rf.get("/fake-url")

        response = batch_task_list_view(request)

        assert response.status_code == 200
