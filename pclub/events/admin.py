from django.contrib import admin
from.models import Events, Images
# Register your models here.

class ImagesAdmin(admin.StackedInline):
    model = Images

@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    inlines = [ImagesAdmin]

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    pass    
