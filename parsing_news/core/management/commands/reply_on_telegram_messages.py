from time import sleep

import logging
from django.core.management.base import BaseCommand

from core import models, tasks

logger = logging.getLogger('tasks')


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Telegram reply messages run')

        while True:
            tasks.reply_on_telegram_messages()

            # try:
            #     tasks.reply_on_telegram_messages()
            # except Exception as e:
            #     logger.warning('bot_error \t' + str(e), 'reply_on_telegram_messages.log')

            sleep(10)
