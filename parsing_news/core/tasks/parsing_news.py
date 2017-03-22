import logging
from core import models

logger = logging.getLogger('tasks')


def parsing_news(*args, **kwargs):
    for site in models.SiteNews.objects.filter(bots__users__isnull=False).distinct():
        try:
            site.get_news()
        except Exception as e:
            print('exception! news_sites: ' + str(e))
            logger.warning(str(e), 'parsing_news_sites.log')
