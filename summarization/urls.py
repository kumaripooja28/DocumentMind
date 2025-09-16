"""
URL routing for AI summarization endpoints.

This module defines API endpoints for direct text summarization services
that don't require document upload or storage.
"""

from django.urls import path
from .views import SummarizeTextView

urlpatterns = [
    # Direct text summarization endpoint - accepts raw text and returns AI-generated summaries
    path('summarize-text/', SummarizeTextView.as_view(), name='summarize-text'),
]
