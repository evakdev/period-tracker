from django.contrib import admin, messages
from django.contrib.messages.api import add_message

from .models import *

# Register your models here.

class testinline(admin.StackedInline):
    model=Trackable
    extra=0
class testTabular(admin.TabularInline):
    model=Trackable
    extra=0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name','pk']
    sortable_by=['name']
    search_fields=['name','pk']
    inlines = [testinline]
    list_filter=['name']
    
   


@admin.register(Trackable)
class TrackableAdmin(admin.ModelAdmin):
    list_display=['id','name','category','pk']
    list_filter=['category','name']
    list_editable=['category']
    readonly_fields=['name']
    list_display_links=['name']

