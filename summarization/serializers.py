"""
Serializers for direct text summarization API endpoints.

This module defines data validation and formatting for the text summarization
service that accepts raw text input and returns AI-generated summaries.
"""

from rest_framework import serializers


class SummarizeTextSerializer(serializers.Serializer):
    """
    Serializer for text summarization request data.
    
    Validates input text content and summarization mode preferences
    for the direct text summarization API endpoint.
    """
    # Text content to be summarized (required)
    text = serializers.CharField(
        help_text="Raw text content to generate summaries from"
    )
    
    # Summary generation mode (optional, defaults to both types)
    mode = serializers.ChoiceField(
        choices=[
            ('short', 'Short summary only'),
            ('detailed', 'Detailed notes only'),
            ('both', 'Both short summary and detailed notes')
        ],
        default='both',
        help_text="Type of summary to generate"
    )


class SummaryResponseSerializer(serializers.Serializer):
    """
    Serializer for summarization API response data.
    
    Formats the AI-generated summary content for JSON API responses,
    supporting both short summaries and detailed bullet-pointed notes.
    """
    # Brief overview summary (2-3 sentences)
    short_summary = serializers.CharField(
        allow_blank=True,
        help_text="Concise summary for quick overview"
    )
    
    # Detailed bullet-pointed notes
    detailed_notes = serializers.CharField(
        allow_blank=True,
        help_text="Comprehensive bullet-pointed summary"
    )
