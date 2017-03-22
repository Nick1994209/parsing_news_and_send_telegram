from datetime import timedelta

from .parsing_cinema import parsing_cinema
from .parsing_news import parsing_news
from .parsing_rss import parsing_rss
from .reply_on_messages import reply_on_telegram_messages


def celery_add_periodic_task():
    from parsing_news.celery import app

    app.add_periodic_task(timedelta(hours=4), app.task(parsing_cinema), name='parsing_cinema')
    app.add_periodic_task(timedelta(hours=4), app.task(parsing_news), name='parsing_news')
    app.add_periodic_task(timedelta(hours=2), app.task(parsing_rss), name='parsing_rss')
    app.add_periodic_task(
        timedelta(seconds=10), app.task(reply_on_telegram_messages),
        name='reply_on_telegram_messages'
    )

celery_add_periodic_task()
