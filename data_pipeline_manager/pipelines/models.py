from django.db import models
from django.utils.translation import gettext_lazy as _

from .tasks import run_ocr_import_pipelines


class PipelineTypes(models.TextChoices):
    IMPORT = "I", _("Import")
    REIMPORT = "R", _("Reimport")


class TaskStatus(models.TextChoices):
    RUNNING = "R", _("Running")
    SUCCESS = "S", _("Success")
    FAILURE = "F", _("Failure")


class BatchTask(models.Model):
    name = models.CharField(max_length=255)
    inputs = models.TextField(max_length=10000)
    started_on = models.DateTimeField(auto_now_add=True)
    pipeline_config = models.JSONField()
    pipeline_type = models.CharField(
        max_length=1, choices=PipelineTypes.choices, default=PipelineTypes.IMPORT
    )

    def __str__(self):
        return f"{self.name} ({self.get_pipeline_type_display()})"

    @property
    def inputs_list(self):
        return self.get_inputs()

    def get_inputs(self):
        return [input for input in self.inputs.splitlines() if input]

    def run(self):
        """Start the Batch Task by create tasks and running them"""
        inputs = self.get_inputs()
        for input in inputs:
            task = Task.objects.create(
                batch=self,
                input=input,
                pipeline_config=self.pipeline_config,
            )
            task.run()


class Task(models.Model):
    batch = models.ForeignKey(
        BatchTask, on_delete=models.CASCADE, blank=True, null=True, related_name="tasks"
    )
    celery_task_id = models.CharField(max_length=36)
    started_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    input = models.CharField(max_length=255, null=True, blank=True)
    pipeline_config = models.JSONField(null=True, blank=True)
    result = models.CharField(max_length=32, null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=TaskStatus.choices, default=TaskStatus.RUNNING
    )

    def __str__(self):
        return f"Task {self.input}"

    def start_celery_task(self, task_id, input, config):
        celery_task_id = run_ocr_import_pipelines.delay(task_id, input, **config)
        return celery_task_id

    def run(self):
        celery_task_id = self.start_celery_task(
            self.id, self.input, self.pipeline_config
        )
        self.celery_task_id = celery_task_id
        self.save()

    @property
    def is_completed(self):
        return self.status == TaskStatus.SUCCESS or self.status == TaskStatus.FAILURE
