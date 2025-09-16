"""
User account serializers for the Document Summarizer application.

This module handles user registration data validation and user account
creation with proper security measures including password requirements.
"""

from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration data.
    
    Handles new user account creation with validation for username uniqueness,
    email format, and secure password requirements. Ensures passwords are
    write-only and meet minimum security standards.
    """
    # Password field with security requirements
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        help_text="Password must be at least 8 characters long"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        """
        Create a new user account with encrypted password.
        
        Uses Django's built-in user creation method to ensure proper
        password hashing and user model initialization.
        
        Args:
            validated_data: Cleaned registration data from form submission
            
        Returns:
            Created User instance with encrypted password
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
