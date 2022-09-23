import pytest

from .factories import TaskFactory

pytestmark = pytest.mark.django_db


class TestTask:
    def test_factory(self):
        task = TaskFactory()

        assert task is not None
        assert task.is_completed
