from time import sleep, timezone

from django.core.management.base import BaseCommand
from core import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing news sites run')
        hour = 60 * 60

        while True:
            current_hour = timezone.now().hour  # AM
            if 1 < current_hour < 8:
                sleep((8 - current_hour) * hour)

            for site in models.SiteNews.objects.all():
                site.get_news()

            sleep(6 * hour)
