from django.core.management.base import BaseCommand
from core import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Telegram bot run')

        for bot in models.TelegramBot.objects.all():
            bot = bot.get_bot()
            # telegram_