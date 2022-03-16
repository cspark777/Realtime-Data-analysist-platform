from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_by',
    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'created_by',
                'druid_url',
                'kafka_url'
            )
        }),
    )

    search_fields = (
        'name',
    )
