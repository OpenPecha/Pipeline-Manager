from django.contrib import admin

from .models import BatchTask, Task


@admin.register(BatchTask)
class BatchTaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
