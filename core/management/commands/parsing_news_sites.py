from time import sleep

from django.core.management.base import BaseCommand
from core import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing news sites run')

        while True:
            for site in models.SiteNews.objects.all():
                site.get_news()

            hour = 60 * 60
            sleep(6 * hour)
