from celery import shared_task
from .services import service

@shared_task
def generate_summaries_task(text: str, mode: str = 'both'):
    return service.summarize(text, mode=mode)
