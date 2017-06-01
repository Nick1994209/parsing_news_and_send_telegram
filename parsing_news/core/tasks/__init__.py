from datetime import timedelta

from .parsing_cinema import parsing_cinema
from .parsing_news import parsing_news
from .parsing_rss import parsing_rss
from .reply_on_messages import reply_on_telegram_messages


def celery_add_periodic_task():
    from parsing_news.celery import app

    app.add_periodic_task(timedelta(hours=4), app.task(parsing_cinema), name='parsing_cinema',
                          routing_key='norm')  # soft_time_limit, time_limit TODO
    app.add_periodic_task(timedelta(hours=4), app.task(parsing_news), name='parsing_news',  routing_key='norm')
    app.add_periodic_task(timedelta(hours=2), app.task(parsing_rss), name='parsing_rss',  routing_key='norm')
    app.add_periodic_task(
        timedelta(seconds=10), app.task(reply_on_telegram_messages),
        name='reply_on_telegram_messages',  routing_key='high'
    )

celery_add_periodic_task()
