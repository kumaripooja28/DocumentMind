"""
API views for direct text summarization services.

This module provides endpoints for immediate text summarization without
requiring document upload or storage. Users can submit raw text and receive
AI-generated summaries in real-time.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import SummarizeTextSerializer, SummaryResponseSerializer
from .services import service


class SummarizeTextView(APIView):
    """
    API endpoint for direct text summarization.
    
    Accepts raw text input and returns AI-generated summaries without storing
    the content. Useful for quick summarization tasks or integration with
    external applications.
    """
    # Require user authentication to prevent abuse
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Generate summaries from submitted text content.
        
        Validates input text and summarization mode, then uses the AI service
        to generate appropriate summaries based on user preferences.
        
        Args:
            request: HTTP request containing text and mode parameters
            
        Returns:
            JSON response with generated summaries or validation errors
        """
        # Validate request data
        serializer = SummarizeTextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract validated parameters
        text = serializer.validated_data['text']
        mode = serializer.validated_data['mode']
        
        # Generate summaries using AI service
        summaries = service.summarize(text, mode=mode)
        
        # Format response data
        response_serializer = SummaryResponseSerializer(summaries)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
