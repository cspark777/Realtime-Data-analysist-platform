from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import StreamProcessor, StreamProcessorStep


class InlineSPS(admin.TabularInline):
    model = StreamProcessorStep
    extra = 1


@admin.register(StreamProcessorStep)
class StreamProcessorStepAdmin(MPTTModelAdmin):
    # inlines = (InlineSPS,)
    # specify pixel amount for this ModelAdmin only:
    # mptt_level_indent = 20
    pass


@admin.register(StreamProcessor)
class StreamProcessorAdmin(admin.ModelAdmin):
    inlines = (InlineSPS,)
