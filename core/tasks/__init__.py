from django.db import IntegrityError

from core import create_log
from .parsing_cinema_sites import parsing_cinema_sites
from .parsing_news_sites import parsing_news_sites
from .reply_on_messages import reply_on_telegram_messages

from django_q.tasks import schedule, Schedule


def task_hook(task):
    message = '{task} {func}'.format(task=task.group, func=task.func)
    create_log.create(message, 'tasks.log')


def create_tasks():
    try:
        schedule(
            name='parsing_cinema_sites',
            func=parsing_cinema_sites.__module__,
            schedule_type=Schedule.HOURLY,
            minutes=1
            # repeats=16,
            # next_run=arrow.utcnow().replace(hour=18, minute=0)
        )
    except IntegrityError:  # task existed
        pass

    try:
        schedule(
            name='parsing_news_sites',
            func=parsing_news_sites.__module__,
            schedule_type=Schedule.HOURLY,
            minutes=2,
            # repeats=8,
            # next_run=arrow.utcnow().replace(hour=18, minute=0),
        )
    except IntegrityError:
        pass

    try:
        schedule(
            name='reply_on_telegram_messages',
            func=reply_on_telegram_messages.__module__,
            schedule_type=Schedule.MINUTES,
            minutes=2,
        )
    except IntegrityError:
        pass


def create_tasks_without_models():
    from django_q.tasks import result, async as q_async
    from time import sleep

    task_id = q_async(reply_on_telegram_messages, sync=True)
    sleep(10)
    q_async(reply_on_telegram_messages, hook=task_hook)
