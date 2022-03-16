from django.contrib import admin
from .models import Search


@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    pass

