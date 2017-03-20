from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from core import create_log, models, tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing news sites run')
        hour = 60 * 60

        while True:
            current_hour = timezone.now().hour  # AM
            if 1 < current_hour < 8:
                sleep((8 - current_hour) * hour)

            tasks.parsing_rss()

            sleep(6 * hour)
