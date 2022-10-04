import pytest

from .factories import BatchFactory, TaskFactory

pytestmark = pytest.mark.django_db


class TestBatchTask:
    def test_factroy(self):
        batch = BatchFactory()

        assert batch is not None

    def test_get_inputs(self):
        batch = BatchFactory(inputs="a\nb\nc")

        assert batch.get_inputs() == ["a", "b", "c"]

    def test_run(self):
        batch = BatchFactory(inputs="a\nb\nc")

        batch.run()

        assert batch.tasks.count() == 3


class TestTask:
    def test_factory(self):
        task = TaskFactory()

        assert task is not None
        assert task.is_completed
