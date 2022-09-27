from django.shortcuts import render

from .forms import OCR_ENGINES, OCR_MODELS, OCRTaskForm
from .models import BatchTask, PipelineTypes


def dashboard(request):
    if request.method == "POST":
        form = OCRTaskForm(request.POST)
        if form.is_valid():
            batch = BatchTask.objects.create(
                inputs=form.cleaned_data["inputs"],
                name=form.cleaned_data["name"],
                pipeline_type=PipelineTypes.IMPORT,
                pipeline_config={
                    "ocr_engine": OCR_ENGINES[form.cleaned_data["ocr_engine"]],
                    "model_name": OCR_MODELS[form.cleaned_data["model_name"]],
                },
            )
            batch.save()
    else:
        form = OCRTaskForm()

    context = {"form": form}
    return render(request, "pipelines/dashboard.html", context=context)


def batch_task_lists(request):
    context = {"batch_tasks": BatchTask.objects.all()}
    return render(request, "pipelines/batch_task_lists.html", context=context)
