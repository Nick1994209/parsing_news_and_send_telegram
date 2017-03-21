from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parsing_news.settings')

app = Celery('parsing_news', broker='redis://localhost:6379')
# celery -A parsing_news worker --loglevel=info  --beat  # для schedule

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Europe/London'


# from core.tasks import parsing_cinema, parsing_news, parsing_rss, reply_on_telegram_messages
#
# app.add_periodic_task(timedelta(hours=4), app.task(parsing_cinema))
# app.add_periodic_task(timedelta(hours=4), app.task(parsing_news))
# app.add_periodic_task(timedelta(hours=2), app.task(parsing_rss))
# app.add_periodic_task(timedelta(seconds=10), app.task(reply_on_telegram_messages))

@app.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    print('setup')
    from django.conf import settings
    settings.DEBUG = False

    # app.add_periodic_task(timedelta(seconds=12.0), app.task(a), name='add every 11')
    # app.add_periodic_task(timedelta(seconds=10.0), app.task(a), name='add every 11')

    from ..core.tasks import parsing_cinema, parsing_news, parsing_rss, reply_on_telegram_messages

    app.add_periodic_task(timedelta(hours=4), app.task(parsing_cinema), name='parsing_cinema')
    app.add_periodic_task(timedelta(hours=4), app.task(parsing_cinema), name='parsing_cinema')
    app.add_periodic_task(timedelta(hours=4), app.task(parsing_news), name='parsing_news')
    app.add_periodic_task(timedelta(hours=2), app.task(parsing_rss), name='parsing_rss')
    app.add_periodic_task(timedelta(seconds=10), app.task(reply_on_telegram_messages), name='reply_on_telegram_messages')

    print('all good')


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )
#
#
# @app.task
# def test(arg):
#     print('HIHI', arg)

#
def a():
    print('IM A')
# a.name = 'a'
#
# app.add_periodic_task(timedelta(seconds=10.0), app.task(a), name='add every 11')
# # app.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#
# def debug_task():
#     a = 123
#     print('Request: {0!r}'.format(a))
#
#
# @periodic_task(run_every=(crontab(minute='*/15')), name="some_task", ignore_result=True)
# def some_task():
#     with open('123213', 'w') as file:
#         file.write('123')
#
#     print('hello some_task')
#
#
# @periodic_task(run_every=timedelta(seconds=10))
# def a():
#     return ' i running periodic task '
