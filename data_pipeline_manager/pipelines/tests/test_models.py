import pytest

from .factories import BatchFactory, TaskFactory

pytestmark = pytest.mark.django_db


class TestBatchTask:
    def test_factroy(self):
        batch = BatchFactory()

        assert batch is not None


class TestTask:
    def test_factory(self):
        task = TaskFactory()

        assert task is not None
        assert task.is_completed
