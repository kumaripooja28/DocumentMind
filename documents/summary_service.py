from typing import Tuple
from summarization.services import service as summarization_service


def generate_document_summaries(text: str) -> Tuple[str, str]:
    """Generate short & detailed summaries for a document's text.
    Returns (short_summary, detailed_notes).
    """
    # We call the underlying service twice via its combined interface to keep logic centralized.
    result = summarization_service.summarize(text, mode='both')
    return result.get('short_summary', ''), result.get('detailed_notes', '')
