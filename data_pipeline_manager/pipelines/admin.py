from django.contrib import admin

from .models import BatchTask


@admin.register(BatchTask)
class BatchTaskAdmin(admin.ModelAdmin):
    pass
