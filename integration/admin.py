from django.contrib import admin
from integration.models import *
# Register your models here.
admin.register(DataSource)

class DataSourceAdmin(admin.ModelAdmin):
    pass
