"""
Text extraction service for the Document Summarizer application.

This module handles extracting readable text content from various document formats
including PDF, DOCX, and plain text files. It provides secure, size-limited
extraction with proper error handling.
"""

from django.conf import settings
from typing import IO
import fitz  # PyMuPDF for PDF processing
from docx import Document as DocxDocument

# File formats supported by the extraction service
SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}


class ExtractionError(Exception):
    """Exception raised when document text extraction fails."""
    pass


def _read_txt(stream: IO[bytes]) -> str:
    """
    Extract text from plain text files with encoding detection.
    
    Args:
        stream: File stream containing text content
        
    Returns:
        Extracted text content as string
    """
    stream.seek(0)
    content = stream.read()
    
    # Try UTF-8 first (most common), fallback to latin-1 for compatibility
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        return content.decode('latin-1', errors='replace')


def _read_pdf(stream: IO[bytes]) -> str:
    """
    Extract text content from PDF documents.
    
    Uses PyMuPDF (fitz) to parse PDF structure and extract readable text
    from all pages while preserving basic formatting.
    
    Args:
        stream: File stream containing PDF document
        
    Returns:
        Combined text content from all PDF pages
    """
    data = stream.read()
    with fitz.open(stream=data, filetype='pdf') as doc:
        page_texts = []
        for page in doc:
            page_texts.append(page.get_text())
    return '\n'.join(page_texts)


def _read_docx(stream: IO[bytes]) -> str:
    """
    Extract text content from Microsoft Word documents.
    
    Processes DOCX files to extract paragraph text while filtering out
    empty paragraphs and preserving document structure.
    
    Args:
        stream: File stream containing DOCX document
        
    Returns:
        Combined text content from all document paragraphs
    """
    # python-docx requires file stream positioned at beginning
    stream.seek(0)
    document = DocxDocument(stream)
    
    # Extract non-empty paragraphs and join with newlines
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return '\n'.join(paragraphs)


def extract_text(file_obj) -> str:
    """
    Extract text content from uploaded document files.
    
    This is the main entry point for text extraction. It validates file size,
    determines the appropriate extraction method based on file extension,
    and applies content length limits for security.
    
    Args:
        file_obj: Django UploadedFile instance containing the document
        
    Returns:
        Extracted text content, truncated if necessary
        
    Raises:
        ExtractionError: If file is too large, unsupported format, or extraction fails
    """
    filename = file_obj.name.lower()
    file_size_mb = file_obj.size / (1024 * 1024)
    
    # Validate file size to prevent memory issues and abuse
    if file_size_mb > settings.MAX_DOCUMENT_SIZE_MB:
        raise ExtractionError(
            f"File exceeds maximum size limit of {settings.MAX_DOCUMENT_SIZE_MB}MB"
        )

    # Route to appropriate extraction method based on file extension
    if filename.endswith('.pdf'):
        file_obj.seek(0)
        text = _read_pdf(file_obj)
    elif filename.endswith('.docx'):
        file_obj.seek(0)
        text = _read_docx(file_obj)
    elif filename.endswith('.txt'):
        file_obj.seek(0)
        text = _read_txt(file_obj)
    else:
        raise ExtractionError("Unsupported file type. Supported formats: PDF, DOCX, TXT")

    # Clean up and apply length limits for processing efficiency
    text = text.strip()
    if len(text) > settings.MAX_EXTRACT_CHAR:
        text = text[:settings.MAX_EXTRACT_CHAR]
        
    return text
