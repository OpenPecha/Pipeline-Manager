from django.db import models
from django.utils.translation import gettext_lazy as _


class PipelineTypes(models.TextChoices):
    IMPORT = "I", _("Import")
    REIMPORT = "R", _("Reimport")


class BatchTask(models.Model):
    name = models.CharField(max_length=255)
    inputs = models.TextField(max_length=10000)
    started_on = models.DateTimeField(auto_now_add=True)
    pipeline_config = models.JSONField()
    metadata = models.JSONField(null=True, blank=True)
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

    @property
    def pipeline_config_display(self):
        striped_config = {}
        keys_to_exclude = ["credentials", "images_path", "ocr_outputs_path"]
        for key, value in self.pipeline_config.items():
            if key not in keys_to_exclude:
                striped_config[key] = value
        return striped_config


class TaskStatus(models.TextChoices):
    RUNNING = "R", _("Running")
    SUCCESS = "S", _("Success")
    FAILURE = "F", _("Failure")


class Task(models.Model):
    batch = models.ForeignKey(
        BatchTask, on_delete=models.CASCADE, blank=True, null=True, related_name="tasks"
    )
    celery_task_id = models.CharField(max_length=36)
    started_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    input = models.CharField(max_length=255, null=True, blank=True)
    pipeline_config = models.JSONField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=TaskStatus.choices, default=TaskStatus.RUNNING
    )

    def __str__(self):
        return f"Task {self.input}"

    @property
    def is_completed(self):
        return self.status == TaskStatus.SUCCESS or self.status == TaskStatus.FAILURE
