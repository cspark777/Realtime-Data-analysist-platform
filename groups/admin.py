from django.contrib import admin

from .models import StreamGroup, StreamProcessorGroup, SimulationGroup

admin.site.register(StreamGroup)
admin.site.register(StreamProcessorGroup)
admin.site.register(SimulationGroup)
