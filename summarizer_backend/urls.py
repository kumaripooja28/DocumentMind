"""
Main URL configuration for the Document Summarizer backend.

This module defines the root URL routing for the application, connecting
different app endpoints and enabling static file serving in development mode.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Main application URL routing
urlpatterns = [
    # Django admin interface for database management
    path('admin/', admin.site.urls),
    
    # User authentication endpoints (register, login, token refresh)
    path('api/auth/', include('accounts.urls')),
    
    # DRF browsable API authentication (for login/logout in web interface)
    path('api-auth/', include('rest_framework.urls')),
    
    # AI summarization service endpoints
    path('api/', include('summarization.urls')),
    
    # Document upload and management endpoints
    path('api/', include('documents.urls')),
]

# Serve uploaded files during development
# In production, use a proper web server (nginx, Apache) for static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
