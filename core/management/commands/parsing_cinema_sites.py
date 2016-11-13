from time import sleep

import datetime
from django.core.management.base import BaseCommand
from core import models
from django.utils import timezone
from core import create_log


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing cinema sites run')
        hour = 60 * 60

        while True:
            now = timezone.now()
            current_hour = now.hour # AM
            if 1 < current_hour < 8:
                sleep((8 - current_hour) * hour)

            self.parsing()

            two_month_ago = now - datetime.timedelta(days=60)
            models.TVSeries.objects.filter(
                date_release_last_ongoing_series__lte=two_month_ago
            ).delete()

            sleep(1 * hour)

    def parsing(self):
        for site in models.SiteCinema.objects.all():
            try:
                site.get_new_episodes()
            except Exception as e:
                print('exception! cinema_sites: ' + str(e))
                create_log.create(str(e), 'parsing_cinema_sites.log')
