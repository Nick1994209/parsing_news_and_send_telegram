import datetime

from django.utils import timezone

from core import create_log, models


def parsing_cinema_sites(*args, **kwargs):
    parsing()
    delete_old_tvseries()


def parsing():
    for site in models.SiteCinema.objects.filter(bots__users__isnull=False):
        try:
            site.get_new_episodes()
        except Exception as e:
            print('exception! cinema_sites: ' + str(e))
            create_log.create(str(e), 'parsing_cinema_sites.log')


def delete_old_tvseries():
    now = timezone.now()
    month_ago = now - datetime.timedelta(days=30)
    models.TVSeries.objects.filter(date_release_last_ongoing_series__lte=month_ago) \
        .delete()
