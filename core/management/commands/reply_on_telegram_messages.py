from time import sleep

from django.core.management.base import BaseCommand
from core import models


GET_SITES = '/start'
GET_TV_SERIES_FOR = '/site_cinema__'
ALERTING_FOR_NEWS = '/site_news__'
ALERTING_FOR_TV_SERIES = '/tv_series__'


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Telegram reply messages run')

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
                    self.get_command(bot_user, message)

            sleep(10)

    @staticmethod
    def get_command(bot_user, message):
        command = message['text']
        if command == GET_SITES:
            message_ser = 'Вы можете выбрать один из сайтов с сериалами: \n'
            message_serials = message_ser + models.SiteCinema.get_all_sites(command=GET_TV_SERIES_FOR)
            message_n = 'Вы можете выбрать один из сайтов с новостями: \n'
            message_news = message_n + models.SiteNews.get_all_sites(command=ALERTING_FOR_NEWS)
            bot_user.send_message(message_serials + message_news)

        if command.startswith(GET_TV_SERIES_FOR):
            site_name = command.split(GET_TV_SERIES_FOR).pop()
            site = models.Site.objects.get(name=site_name)
            message = 'Вы можете подпасаться на следующие сериалы:\n'
            tv_series = [tv_series.name_rus + ' ' + ALERTING_FOR_TV_SERIES + str(tv_series.id)
                         for tv_series in site.tv_series.all()]
            count_tv_series = len(tv_series)
            count_in_page = 40
            if count_tv_series % count_in_page == 0:
                pages = count_tv_series/count_in_page
            else:
                pages = int(count_tv_series / count_in_page) + 1
            for page in range(pages):
                bot_user.send_message(message + '\n'.join(tv_series[page*count_in_page:page*count_in_page+count_in_page]))

        if command.startswith(ALERTING_FOR_NEWS):
            news_name = command.split(ALERTING_FOR_NEWS).pop()
            news = models.SiteNews.objects.get(name=news_name)
            news.users.create(bot_user) # add
            bot_user.send_message('Подписаны на новости {}'.format(news_name))

        if command.startswith(ALERTING_FOR_TV_SERIES):
            tv_series_id = command.split(ALERTING_FOR_TV_SERIES).pop()
            tv_series = models.SiteTVSeries.objects.filter(id=tv_series_id)
            if tv_series:
                tv_series = tv_series[0]
                if bot_user.tv_series.filter(tv_series=tv_series):
                    bot_user.send_message('Вы уже подписаны на {}\n'.format(tv_series.name_rus))
                else:
                    bot_user.tv_series.create(tv_series=tv_series)
                    bot_user.send_message('Теперь вы подписаны на {}\n'.format(tv_series.name_rus))
            else:
                bot_user.send_message('Не найдено сериала ')