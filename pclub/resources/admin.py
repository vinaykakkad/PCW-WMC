from django.contrib import admin
from.models import Tags, Resources, Files, Links
# Register your models here.

admin.site.register(Tags)

class FileAdmin(admin.StackedInline):
    model = Files

class LinkAdmin(admin.StackedInline):
    model = Links

@admin.register(Resources)
class EventsAdmin(admin.ModelAdmin):
    inlines = [FileAdmin, LinkAdmin]

@admin.register(Files)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(Links)
class LinkAdmin(admin.ModelAdmin):
    pass