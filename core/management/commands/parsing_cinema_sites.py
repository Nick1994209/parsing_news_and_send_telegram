from time import sleep

from django.core.management.base import BaseCommand
from core import models
from django.utils import timezone


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing cinema sites run')
        hour = 60 * 60

        while True:
            current_hour = timezone.now().hour # AM
            if 1 < current_hour < 8:
                sleep((8 - current_hour) * hour)

            for site in models.SiteCinema.objects.all():
                site.get_new_episodes()


            sleep(1/2 * hour)
