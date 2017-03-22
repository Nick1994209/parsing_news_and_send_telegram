from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parsing_news.settings')

from django.conf import settings

app = Celery('parsing_news', broker=settings.CELERY_BROKER)
# celery -A parsing_news worker --loglevel=info  --beat  # для schedule

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Europe/London'
