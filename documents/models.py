"""
Database models for the Document Summarizer application.

This module defines the data structure for documents and their summaries,
including user relationships and processing status tracking.
"""

from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    """
    Represents an uploaded document with extracted text content.
    
    Each document belongs to a specific user and contains the original file,
    extracted text content, and metadata about when it was uploaded.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='documents',
        help_text="The user who uploaded this document"
    )
    file = models.FileField(
        upload_to='documents/',
        help_text="The original uploaded file"
    )
    original_filename = models.CharField(
        max_length=255, 
        blank=True,
        help_text="The name of the file when it was uploaded"
    )
    text_content = models.TextField(
        blank=True,
        help_text="Text content extracted from the document"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this document was uploaded"
    )

    def __str__(self):
        """Return a human-readable representation of the document."""
        filename = self.original_filename or self.file.name
        return f"{filename} (uploaded by {self.user.username})"

    class Meta:
        ordering = ['-created_at']  # Show newest documents first
        verbose_name = "Document"
        verbose_name_plural = "Documents"


class Summary(models.Model):
    """
    Represents an AI-generated summary of a document.
    
    Each summary contains both a short version for quick overview and detailed
    notes for comprehensive understanding. The status field tracks the
    processing state for async operations.
    """
    
    # Processing status options
    STATUS_CHOICES = [
        ('pending', 'Waiting to be processed'),
        ('processing', 'Currently being analyzed'),
        ('complete', 'Successfully processed'),
        ('failed', 'Processing failed'),
    ]
    
    document = models.ForeignKey(
        Document, 
        on_delete=models.CASCADE, 
        related_name='summaries',
        help_text="The document this summary belongs to"
    )
    short_summary = models.TextField(
        blank=True,
        help_text="Brief summary for quick overview"
    )
    detailed_notes = models.TextField(
        blank=True,
        help_text="Detailed bullet points covering main topics"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='complete',
        help_text="Current processing status of this summary"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this summary was created"
    )

    def __str__(self):
        """Return a human-readable representation of the summary."""
        return f"Summary for '{self.document.original_filename}' ({self.status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Summary"
        verbose_name_plural = "Summaries"
        constraints = [
            models.UniqueConstraint(
                fields=['document'], 
                name='one_summary_per_document'
            )
        ]
