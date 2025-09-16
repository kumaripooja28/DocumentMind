"""
URL routing for document management endpoints.

This module defines API endpoints for document upload, retrieval, and 
summary management within the Document Summarizer application.
"""

from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import DocumentViewSet

# Create router for standard CRUD operations on documents
router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    # Include all standard document endpoints (list, create, retrieve, update, delete)
    *router.urls,
    
    # Custom endpoint for document summary operations
    # GET: retrieve summary, PATCH: retry failed summary generation
    path(
        'documents/<int:pk>/summary/', 
        DocumentViewSet.as_view({
            'get': 'retrieve_summary', 
            'patch': 'retry_summary'
        }), 
        name='document-summary'
    ),
]