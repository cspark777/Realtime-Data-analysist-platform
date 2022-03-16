from django.contrib import admin
from .models import DataDictionary, DataItem


@admin.register(DataDictionary)
class DataDictionaryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
            )
        }),
    )

    search_fields = (
        'name',
    )


@admin.register(DataItem)
class DataItemAdmin(admin.ModelAdmin):
    list_display = (
        'source_value',
    )
    fieldsets = (
        (None, {
            'fields': (
                'source_value',
                'mapped_value',
                'datadictionary',
            )
        }),
    )

    search_fields = (
        'source_value',
    )
