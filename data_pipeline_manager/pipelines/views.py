from pathlib import Path

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from ocr_pipelines.config import ImportConfig as OcrImportConfig

from data_pipeline_manager.pipelines.forms import OCR_ENGINES, OCRTaskForm
from data_pipeline_manager.pipelines.models import BatchTask, PipelineTypes, Task
from data_pipeline_manager.pipelines.tasks import OcrMetadata, run_ocr_import_pipelines


class PipelineRunner:
    def __init__(self, form: forms.Form):
        self.form = form
        self.data_path = Path.home() / "app_data" / "ocr_pipeline" / "data"
        images_dir = self.data_path / "images"
        ocr_outputs_dir = self.data_path / "ocr_outputs"
        self.config = OcrImportConfig(
            ocr_engine=OCR_ENGINES[self.form.cleaned_data["ocr_engine"]],
            model_type=self.form.cleaned_data["model_type"],
            lang_hint=form.cleaned_data["language_hint"],
            credentials=self.form.cleaned_data["gcloud_service_account_key"],
            images_path=images_dir,
            ocr_outputs_path=ocr_outputs_dir,
        )
        self.metadata = OcrMetadata(
            pipeline_config=self.config,
            sponsor=self.form.cleaned_data["sponsor_name"],
            sponsor_consent=self.form.cleaned_data["sponsor_concent"],
        )

    def create_batch(self) -> BatchTask:
        batch = BatchTask.objects.create(
            name=self.form.cleaned_data["name"],
            inputs=self.form.cleaned_data["inputs"],
            pipeline_type=PipelineTypes.IMPORT,
            pipeline_config=self.config.to_dict(),
            metadata=self.metadata.to_dict(),
        )
        return batch

    def create_task(self, input_: str, batch: BatchTask) -> Task:
        task = Task.objects.create(
            batch=batch,
            input=input_,
            pipeline_config=self.config.to_dict(),
        )
        return task

    def start_celery_task(self, task_id, input):
        celery_task_id = run_ocr_import_pipelines.delay(
            task_id,
            bdrc_scan_id=input,
            config_dict=self.config.to_dict(),
            metadata_dict=self.metadata.to_dict(),
        )
        return celery_task_id

    def run(self) -> None:
        batch = self.create_batch()
        for input in batch.inputs_list:
            task = self.create_task(input, batch)
            celery_task_id = self.start_celery_task(task.id, input)
            task.celery_task_id = celery_task_id
            task.save()


def dashboard(request):
    if request.method == "POST":
        form = OCRTaskForm(request.POST)
        if form.is_valid():
            pipeline_runner = PipelineRunner(form)
            pipeline_runner.run()
            return HttpResponseRedirect(reverse_lazy("pipelines:dashboard"))
    else:
        form = OCRTaskForm()

    latest_ten_batches = BatchTask.objects.order_by("-started_on")[:10]
    context = {"form": form, "batch_tasks": latest_ten_batches}

    return render(request, "pipelines/dashboard.html", context=context)


class BatchTaskListView(generic.ListView):
    model = BatchTask
    paginate_by = 10
    template_name = "pipelines/batch_task_lists.html"
    context_object_name = "batch_tasks"


batch_task_list_view = BatchTaskListView.as_view()


class BatchTaskDetailView(generic.DetailView):
    model = BatchTask
    template_name = "pipelines/batch_task_detail.html"
    context_object_name = "batch"


batch_task_detail_view = BatchTaskDetailView.as_view()


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = "pipelines/task_detail.html"
    context_object_name = "task"


task_detail_view = TaskDetailView.as_view()
