from utils import create_log
from core import models


def parsing_news(*args, **kwargs):
    for site in models.SiteNews.objects.filter(bots__users__isnull=False).distinct():
        try:
            site.get_news()
        except Exception as e:
            print('exception! news_sites: ' + str(e))
            create_log.create(str(e), 'parsing_news_sites.log')
