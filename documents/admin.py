from django.contrib import admin
from .models import Document, Summary

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_filename', 'created_at')
    search_fields = ('original_filename', 'user__username')

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'created_at')
    search_fields = ('document__original_filename',)
