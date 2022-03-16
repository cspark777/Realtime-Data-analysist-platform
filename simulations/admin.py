from django.contrib import admin

from .models import Simulation, Step


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_by',
    )
    fieldsets = (
        (None, {
            'fields': (
                'project',
                'name',
                'description',
                'created_by',
                'group'
            )
        }),
    )

    search_fields = (
        'name',
    )


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'topic',
        'simulation',
    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'topic',
                'event',
                'delay',
                'ordering',
                'simulation',
            )
        }),
    )

    search_fields = (
        'name',
        'topic',
    )
