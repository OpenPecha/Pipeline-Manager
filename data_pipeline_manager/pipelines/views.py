from django.shortcuts import render

from .forms import OCRTaskForm


def dashboard(request):
    form = OCRTaskForm()

    context = {"form": form}
    return render(request, "pipelines/dashboard.html", context=context)
