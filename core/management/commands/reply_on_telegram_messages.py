from time import sleep

from django.core.management.base import BaseCommand

from core import create_log, models, tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Telegram reply messages run')

        while True:
            try:
                tasks.reply_on_telegram_messages()
            except Exception as e:
                create_log.create('bot_error \t' + str(e), 'reply_on_telegram_messages.log')

            sleep(10)
