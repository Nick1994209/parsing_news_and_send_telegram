from time import sleep

from django.core.management.base import BaseCommand
from core import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Parsing cinema sites run')

        while True:

            for site in models.SiteCinema.objects.all():
                site.get_new_episodes()

            hour = 60 * 60
            sleep(1/2 * hour)
