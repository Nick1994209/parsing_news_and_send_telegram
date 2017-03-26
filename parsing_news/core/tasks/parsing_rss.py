import logging
from datetime import datetime, timedelta

from core import models

logger = logging.getLogger('tasks')
DAYS_FOR_DELETE_OLD_NEWS = 30 * 4  # 4 months


def parsing_rss(*args, **kwargs):
    # parsing new
    for rss in models.Rss.objects.filter(bots__users__isnull=False).distinct().iterator():
        try:
            new_rss_news = rss.get_news()
            message = """На rss канале "{channel}"
            {title}
            {url}
            {description}
            """
            for rss_news in new_rss_news:
                rss_news_message = message.format(
                    channel=rss_news.rss.name,
                    title=rss_news.title,
                    url=rss_news.url,
                    description=rss_news.description,
                )
                rss.users_send_message(rss_news_message)
        except Exception as e:
            logger.exception(e)

    # deleting old
    now = datetime.now()
    months_before_now = now - timedelta(days=DAYS_FOR_DELETE_OLD_NEWS)
    models.RssNews.objects.filter(date_created__lte=months_before_now).delete()
