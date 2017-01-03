from django.db import IntegrityError

from core import create_log
from .parsing_cinema_sites import parsing_cinema_sites
from .parsing_news_sites import parsing_news_sites
from .reply_on_telegram_messages import reply_on_telegram_messages

from django_q.tasks import schedule, Schedule


def task_hook(task):
    message = '{task}'.format(task='hz kakoi task')  # task.__name__
    create_log.create(message, 'tasks.log')


def create_tasks():
    print(parsing_cinema_sites.__module__)
    try:
        schedule(
            name='parsing_cinema_sites',
            func=parsing_cinema_sites.__module__,
            schedule_type=Schedule.MINUTES,
            minutes=30,
        )
    except IntegrityError:
        pass
    schedule(
        name='parsing_news_sites',
        func=parsing_news_sites.__module__,
        hook=task_hook,
        # schedule_type=Schedule.ONCE,
        # minutes=60*3,
        repeats=1
    )

    schedule(
        name='reply_on_telegram_messages',
        func=reply_on_telegram_messages.__module__,
        hook=task_hook,
        # schedule_type=Schedule.ONCE,
        # minutes=3,
        repeats=1
    )


def create_tasks_without_models():
    from django_q.tasks import result, async as q_async
    from time import sleep

    task_id = q_async(reply_on_telegram_messages, sync=True)
    print(result(task_id))
    sleep(10)
    q_async(reply_on_telegram_messages, hook=task_hook)
