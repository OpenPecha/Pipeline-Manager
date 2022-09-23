from factory import Faker
from factory.django import DjangoModelFactory


class TaskFactory(DjangoModelFactory):

    celery_task_id = Faker("uuid4")
    name = Faker("name")
    started_on = Faker("date_time")
    pipeline_type = Faker("random_element", elements=("I", "R"))
    pipeline_config = Faker("json", num_rows=1)
    status = Faker("random_element", elements=("S", "F"))
    completed_on = Faker("date_time")
    result = Faker("pystr")
    error = Faker("pystr")

    class Meta:
        model = "pipelines.Task"
