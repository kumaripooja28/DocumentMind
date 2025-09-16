from celery import shared_task
from documents.models import Document, Summary
from documents.summary_service import generate_document_summaries

@shared_task
def generate_document_summary_async(document_id: int):
    """Generate summary for a document asynchronously via Celery."""
    try:
        doc = Document.objects.get(id=document_id)
        summary = doc.summaries.first()
        
        if summary and summary.status == 'pending':
            # Update to processing status
            summary.status = 'processing'
            summary.save()
            
            # Generate summaries
            short_s, detailed = generate_document_summaries(doc.text_content)
            
            # Update with results
            summary.short_summary = short_s
            summary.detailed_notes = detailed
            summary.status = 'complete'
            summary.save()
            
            return f"Summary generated for document {document_id}"
        else:
            return f"No pending summary found for document {document_id}"
            
    except Document.DoesNotExist:
        return f"Document {document_id} not found"
    except Exception as e:
        # Mark as failed
        if 'summary' in locals():
            summary.status = 'failed'
            summary.detailed_notes = f'Generation failed: {str(e)}'
            summary.save()
        return f"Error generating summary for document {document_id}: {str(e)}"