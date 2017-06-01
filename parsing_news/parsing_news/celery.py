from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parsing_news.settings')
from kombu import Exchange, Queue, binding

from django.conf import settings

app = Celery('parsing_news', broker=settings.CELERY_BROKER)
# celery -A parsing_news worker --loglevel=info  --beat  # для schedule

CELERY_QUEUES = (
    Queue('high', Exchange('high'), routing_key='high'),
    Queue('normal', Exchange('normal'), routing_key='normal'),
    Queue('low', Exchange('low'), routing_key='low'),
)

app.conf.task_queues = CELERY_QUEUES
app.conf.task_default_queue = 'normal'
app.conf.task_default_exchange = 'normal'
app.conf.task_default_routing_key = 'normal'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Europe/London'
