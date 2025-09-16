"""
API serializers for the Document Summarizer application.

This module defines how document and summary data is converted between
Python objects and JSON for API responses. It ensures proper data
validation and formatting for client consumption.
"""

from rest_framework import serializers
from .models import Document, Summary


class SummarySerializer(serializers.ModelSerializer):
    """
    Serializer for summary data returned by the API.
    
    Converts Summary model instances to JSON format for API responses,
    including both short summaries and detailed notes with timestamps.
    """
    class Meta:
        model = Summary
        fields = ['id', 'short_summary', 'detailed_notes', 'created_at']


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for document data and associated summaries.
    
    Handles document upload data and automatically includes related
    summary information in API responses. Text content is read-only
    as it's extracted automatically during upload processing.
    """
    # Include related summaries in the response
    summaries = SummarySerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 
            'original_filename', 
            'file', 
            'text_content', 
            'created_at', 
            'summaries'
        ]
        # Prevent text_content modification via API since it's auto-extracted
        read_only_fields = ['text_content']
