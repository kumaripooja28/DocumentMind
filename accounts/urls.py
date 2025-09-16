"""
URL routing for user authentication endpoints.

This module defines API endpoints for user account management including
registration, login, and JWT token refresh functionality.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    # User registration endpoint - allows new users to create accounts
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT login endpoint - authenticates users and returns access/refresh tokens
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # JWT token refresh endpoint - generates new access tokens using refresh tokens
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
