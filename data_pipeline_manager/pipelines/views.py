from django.http import HttpResponse
from django.shortcuts import render

from .forms import OCRTaskForm


def dashboard(request):
    if request.method == "POST":
        form = OCRTaskForm(request.POST)
        if form.is_valid():
            return HttpResponse(form.cleaned_data.items())
    else:
        form = OCRTaskForm()

    context = {"form": form}
    return render(request, "pipelines/dashboard.html", context=context)
