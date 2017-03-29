import logging
from datetime import datetime, timedelta

from core import models

logger = logging.getLogger('tasks')

DAYS_FOR_DELETE_OLD_NEWS = 30 * 4  # 4 months


def parsing_news(*args, **kwargs):
    # parsing
    for site in (models.SiteNews.objects
                         .filter(bots__users__isnull=False)
                         .distinct()
                         .iterator()):
        try:
            site.get_news()
        except Exception as e:
            logger.exception(e)
            logger.warning(str(e))

    # deleting old
    now = datetime.now()
    months_before_now = now - timedelta(days=DAYS_FOR_DELETE_OLD_NEWS)
    models.News.objects.filter(date_created__lte=months_before_now).delete()
