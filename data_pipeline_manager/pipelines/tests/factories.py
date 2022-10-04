import factory
from factory import Faker
from factory.django import DjangoModelFactory


class BatchFactory(DjangoModelFactory):
    class Meta:
        model = "pipelines.BatchTask"

    inputs = Faker("text")
    name = Faker("name")
    pipeline_config = Faker("json", num_rows=1)
    pipeline_type = Faker("random_element", elements=("I", "R"))


class TaskFactory(DjangoModelFactory):

    batch = factory.SubFactory(BatchFactory)
    input = Faker("text")
    celery_task_id = Faker("uuid4")
    started_on = Faker("date_time")
    status = Faker("random_element", elements=("S", "F"))
    completed_on = Faker("date_time")
    result = Faker("pystr")
    error = Faker("pystr")

    class Meta:
        model = "pipelines.Task"
