from django.urls import path

from . import views

app_name = "pipelines"
urlpatterns = [
    path("", view=views.dashboard, name="dashboard"),
    path("batches/", view=views.batch_task_list_view, name="batch_tasks_list"),
]
