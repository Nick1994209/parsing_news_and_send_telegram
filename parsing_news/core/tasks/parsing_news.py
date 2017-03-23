import logging
from core import models

logger = logging.getLogger('tasks')


def parsing_news(*args, **kwargs):
    for site in models.SiteNews.objects.filter(bots__users__isnull=False).distinct():
        try:
            site.get_news()
        except Exception as e:
            logger.exception(e)
