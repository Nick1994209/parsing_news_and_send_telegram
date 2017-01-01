from time import sleep

import datetime
from django.core.management.base import BaseCommand
from core import models
from django.utils import timezone
from core import create_log


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing cinema sites run')

        while True:
            self.parsing()
            self.delete_old_tvseries()
            self.grab_sleep()

    def grab_sleep(self):
        hour = 60 * 60

        now = timezone.now()
        current_hour = now.hour  # AM

        # night
        if 1 < current_hour < 8:
            sleep((8 - current_hour) * hour)
        else:
            sleep(1 * hour)

    def parsing(self):
        for site in models.SiteCinema.objects.filter(bots__users__isnull=False):
            try:
                site.get_new_episodes()
            except Exception as e:
                print('exception! cinema_sites: ' + str(e))
                create_log.create(str(e), 'parsing_cinema_sites.log')

    def delete_old_tvseries(self):
        now = timezone.now()
        month_ago = now - datetime.timedelta(days=30)
        models.TVSeries.objects.filter(date_release_last_ongoing_series__lte=month_ago)\
            .delete()
