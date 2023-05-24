from django.urls import path

from . import views

app_name = "pipelines"
urlpatterns = [
    path("", view=views.dashboard, name="dashboard"),
    path("batches/", view=views.batch_task_list_view, name="batch_tasks_list"),
    path("batches/<int:pk>/", view=views.batch_task_detail_view, name="batch_detail"),
    path("tasks/<int:pk>/", view=views.task_detail_view, name="task_detail"),
    path("tasks/search/", views.task_search_view, name="task_search"),
]
