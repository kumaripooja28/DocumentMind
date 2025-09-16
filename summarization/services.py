"""
AI-powered text summarization service for the Document Summarizer application.

This module provides intelligent text summarization using HuggingFace transformers.
It generates both short summaries for quick overviews and detailed notes for
comprehensive understanding of document content.
"""

from django.conf import settings
from functools import lru_cache
from typing import Dict, Any


class SummarizationService:
    """
    Service class for generating AI-powered text summaries.
    
    This service uses HuggingFace transformers to create intelligent summaries
    of text content. It supports multiple summary types and gracefully handles
    errors with fallback functionality.
    """
    
    def __init__(self):
        """Initialize the service with the configured AI model."""
        self.model_name = settings.SUMMARIZATION_MODEL_NAME

    @lru_cache(maxsize=1)
    def _get_pipeline(self) -> Any:
        """
        Get or create the AI summarization pipeline.
        
        This method loads the AI model on first use and caches it for better
        performance. If the model fails to load, it provides a simple fallback
        that returns basic text snippets.
        
        Returns:
            The summarization pipeline or a fallback dummy object
        """
        try:
            # Import transformers only when needed to avoid slowing down
            # Django management commands and database migrations
            from transformers import pipeline
            return pipeline("summarization", model=self.model_name)
        except Exception:
            # Fallback implementation for cases where the AI model
            # cannot be loaded (missing dependencies, network issues, etc.)
            class SimpleFallback:
                """Basic fallback that returns text snippets when AI is unavailable."""
                def __call__(self, text, max_length=60, min_length=15, do_sample=False):
                    # Return first two sentences up to max_length
                    sentences = text.strip().split('.')[:2]
                    result = '. '.join(sentences)[:max_length]
                    return [{"summary_text": result}]
            return SimpleFallback()

    def summarize(self, text: str, mode: str = 'both') -> Dict[str, str]:
        """
        Generate summaries from input text.
        
        Args:
            text: The text content to summarize
            mode: Summary type - 'short', 'detailed', or 'both'
        
        Returns:
            Dictionary containing requested summary types:
            - short_summary: Brief overview (2-3 sentences)
            - detailed_notes: Bullet-pointed key information
        """
        pipeline = self._get_pipeline()
        result = {}
        text = text.strip()
        
        # Handle empty text input
        if not text:
            return {"short_summary": "", "detailed_notes": ""}

        # Generate short summary if requested
        if mode in ('short', 'both'):
            # Create concise summary for quick overview
            summary_output = pipeline(
                text, 
                max_length=settings.SUMMARY_SHORT_MAX_LEN, 
                min_length=settings.SUMMARY_SHORT_MIN_LEN, 
                do_sample=False
            )[0]["summary_text"]
            result['short_summary'] = summary_output
            
        # Generate detailed notes if requested
        if mode in ('detailed', 'both'):
            # Create comprehensive summary for in-depth understanding
            detailed_output = pipeline(
                text, 
                max_length=settings.SUMMARY_DETAILED_MAX_LEN, 
                min_length=settings.SUMMARY_DETAILED_MIN_LEN, 
                do_sample=False
            )[0]["summary_text"]
            
            # Convert summary into bullet points for better readability
            # Split by sentences and format as bulleted list
            sentences = [seg.strip() for seg in detailed_output.split('.') if seg.strip()]
            bullets = '- ' + '\n- '.join(sentences)
            result['detailed_notes'] = bullets
            
        # Ensure both fields are present in response for consistency
        if mode == 'short':
            result.setdefault('detailed_notes', '')
        if mode == 'detailed':
            result.setdefault('short_summary', '')
            
        return result


# Global service instance for use throughout the application
# This singleton pattern ensures consistent model loading and caching
service = SummarizationService()
