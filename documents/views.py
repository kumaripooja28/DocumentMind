"""
Document management views for the Document Summarizer application.

This module handles document upload, text extraction, and summary generation.
It provides a RESTful API for users to upload documents and retrieve their
automatically generated summaries.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document, Summary
from .serializers import DocumentSerializer
from .extraction import extract_text, ExtractionError
from .summary_service import generate_document_summaries


class DocumentViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing documents and their summaries.
    
    This viewset provides the following functionality:
    - Upload documents (PDF, DOCX, TXT files)
    - Extract text content automatically
    - Generate AI-powered summaries
    - Retrieve document lists and individual summaries
    - Delete documents
    
    All operations are restricted to authenticated users and users can only
    access their own documents.
    """
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Support file uploads

    def get_queryset(self):
        """Return documents belonging to the current user, newest first."""
        return Document.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """
        Handle document upload and processing.
        
        This method:
        1. Validates the uploaded file
        2. Extracts text content from the document
        3. Saves the document to the database
        4. Generates summaries (sync for small docs, async for large ones)
        """
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({
                'detail': 'Please provide a file to upload'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract text content from the uploaded file
        try:
            extracted = extract_text(file_obj)
        except ExtractionError as e:
            return Response({
                'detail': f'Unable to process file: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doc: Document = serializer.save(user=request.user, original_filename=file_obj.name, text_content=extracted)
        
        # Branch: sync for small docs, async for large
        from django.conf import settings
        if len(extracted) > settings.AUTO_SUMMARY_MAX_CHAR:
            # Large document: create pending summary and enqueue async task
            summary = Summary.objects.create(document=doc, short_summary='', detailed_notes='', status='pending')
            from summarization.async_tasks import generate_document_summary_async
            generate_document_summary_async.delay(doc.id)
        else:
            # Small document: generate summary synchronously
            try:
                short_s, detailed = generate_document_summaries(extracted)
                Summary.objects.create(document=doc, short_summary=short_s, detailed_notes=detailed, status='complete')
            except Exception as e:  # pragma: no cover
                # Fail gracefully without blocking upload
                Summary.objects.create(document=doc, short_summary='', detailed_notes=f'Generation failed: {e}', status='failed')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve_summary(self, request, pk=None):
        doc = self.get_queryset().filter(pk=pk).first()
        if not doc:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        summary = doc.summaries.first()
        if not summary:
            return Response({'detail': 'Summary missing'}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            'document_id': doc.id,
            'status': summary.status,
            'short_summary': summary.short_summary,
            'detailed_notes': summary.detailed_notes,
            'created_at': summary.created_at,
        }
        
        # Add helpful messages for async states
        if summary.status == 'pending':
            response_data['message'] = 'Summary generation queued. Please check back shortly.'
        elif summary.status == 'processing':
            response_data['message'] = 'Summary is being generated. Please check back in a moment.'
        elif summary.status == 'failed':
            response_data['message'] = 'Summary generation failed. You can retry using PATCH.'
            
        return Response(response_data)

    def retry_summary(self, request, pk=None):
        """Manually retry summary generation for failed summaries."""
        doc = self.get_queryset().filter(pk=pk).first()
        if not doc:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        summary = doc.summaries.first()
        if not summary:
            return Response({'detail': 'Summary missing'}, status=status.HTTP_404_NOT_FOUND)
        
        if summary.status != 'failed':
            return Response({'detail': 'Summary is not in failed state'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reset to pending and re-enqueue
        summary.status = 'pending'
        summary.short_summary = ''
        summary.detailed_notes = ''
        summary.save()
        
        from summarization.async_tasks import generate_document_summary_async
        generate_document_summary_async.delay(doc.id)
        
        return Response({'message': 'Summary generation retried'}, status=status.HTTP_200_OK)
