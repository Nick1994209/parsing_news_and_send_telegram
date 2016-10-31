from time import sleep

from django.core.management.base import BaseCommand
from core import models
from django.utils import timezone
from core import create_log


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing news sites run')
        hour = 60 * 60

        while True:
            current_hour = timezone.now().hour  # AM
            if 1 < current_hour < 8:
                sleep((8 - current_hour) * hour)

            try:
                self.parsing()
            except Exception as e:
                create_log.create(str(e), 'parsing_news_sites.log')

            sleep(6 * hour)

    def parsing(self):
        for site in models.SiteNews.objects.all():
            site.get_news()
