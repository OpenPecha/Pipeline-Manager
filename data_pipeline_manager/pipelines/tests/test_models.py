import pytest

from .factories import BatchFactory, TaskFactory

pytestmark = pytest.mark.django_db


class TestBatchTask:
    def test_factroy(self):
        batch = BatchFactory()

        assert batch is not None

    def test__str__(self):
        batch = BatchFactory(name="Test Batch", pipeline_type="I")

        assert str(batch) == "Test Batch (Import)"

    def test_inputs_list_property(self):
        batch = BatchFactory(inputs="a\nb\nc")

        assert batch.inputs_list == ["a", "b", "c"]

    def test_get_inputs(self):
        batch = BatchFactory(inputs="a\nb\nc")

        assert batch.get_inputs() == ["a", "b", "c"]


class TestTask:
    def test_factory(self):
        task = TaskFactory()

        assert task is not None
        assert task.is_completed

    def test__str__(self):
        task = TaskFactory(input="a")

        assert str(task) == f"Task {task.input}"
