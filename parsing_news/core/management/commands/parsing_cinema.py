import datetime
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from core import models, tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing cinema sites run')

        while True:
            self.delete_old_tvseries()

            tasks.parsing_cinema()
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

    def delete_old_tvseries(self):
        now = timezone.now()
        month_ago = now - datetime.timedelta(days=30)
        (models.TVSeries.objects
         .filter(date_release_last_ongoing_series__lte=month_ago)
         .delete())
