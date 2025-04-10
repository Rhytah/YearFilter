from django.contrib import admin
from .models import PageYear

@admin.register(PageYear)
class PageYearAdmin(admin.ModelAdmin):
    list_display = ('page_id', 'year')
    list_filter = ('year',)
    search_fields = ('page_id', 'year')
    ordering = ('page_id',)