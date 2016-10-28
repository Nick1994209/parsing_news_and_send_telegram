from time import sleep

from django.core.management.base import BaseCommand
from core import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Telegram bot run')

        while True:

            for bot in models.TelegramBot.objects.all():
                for message in bot.get_last_messages():

                    bot_user = bot.users.filter(user_id=message['from']['id'])
                    if bot_user:
                        bot_user = bot_user.get()
                    else:
                        bot_user = bot.users.create(
                            user_id=message['from']['id'], username=message['from'].get('username', ''),
                            first_name=message['from']['first_name'], last_name=message['from'].get('last_name', ''),
                        )
                        bot_user.send_message(models.Site.get_all_sites())

                    self.get_command(bot_user, message)

            sleep(10)

    @staticmethod
    def get_command(bot_user, message):

        command = message['text']
        if command == '/start':
            message = 'Вы можете выбрать один из сайтов с сериалами: \n'
            bot_user.send_message(message + models.Site.get_all_sites(command='/site__'))

        if command.startswith('/site__'):
            site_name = command.split('/site__').pop()
            site = models.Site.objects.get(name=site_name)

            message = 'Вы можете подпасаться на следующие сериалы:\n'
            tv_series = ['/tv_series__'+tv_series.name_rus for tv_series in site.tv_series.all()]
            bot_user.send_message(message + '\n'.join(tv_series))

        if command.startswith('/tv_series__'):
            tv_series_name = command.split('/tv_series__').pop()
            tv_series = models.SiteTVSeries.objects.filter(name_rus__startswith=tv_series_name)

            if tv_series:
                tv_series = tv_series[0]
                if bot_user.tv_series.filter(tv_series=tv_series):
                    bot_user.send_message('Вы уже подписаны на {}\n'.format(tv_series_name))
                else:
                    bot_user.tv_series.create(tv_series=tv_series)
                    bot_user.send_message('Теперь вы подписаны на {}\n'.format(tv_series_name))
            else:
                bot_user.send_message('Не найдено сериала ')