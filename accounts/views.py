"""
User authentication views for the Document Summarizer application.

This module provides API endpoints for user account management including
registration functionality with proper permissions and validation.
"""

from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    Allows new users to create accounts by providing username, email, and password.
    This endpoint is publicly accessible (no authentication required) to enable
    new user sign-ups.
    """
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
