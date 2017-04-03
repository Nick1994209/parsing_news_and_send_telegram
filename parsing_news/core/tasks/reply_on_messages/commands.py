from core import models

GET_SITES = '/start'
GET_TV_SERIES_FOR = '/siteCinema__'
ALERTING_FOR_TV_SERIES = '/tvSeries__'
ALERTING_FOR_NEWS = '/siteNews__'
ALERTING_FOR_RSS = '/siteRSS__'
HELP = '/help'
MY_SUBSCRIPTIONS = '/mySubscriptions__'


class Commands:
    @classmethod
    def run_command(cls, bot_user, message):

        command = message['text'].lstrip('/').split('__')[0]  # example: /start__Vasya123 -> start
        handler = getattr(cls, command, None)
        if handler:
            return handler(bot_user, message)
        else:
            cls.incorrect_command(bot_user, message)

    @classmethod
    def start(cls, bot_user, message):
        cls.getSites(bot_user, message)

    @staticmethod
    def getSites(bot_user, message):
        message_serials = ''
        cinema_sites_names = [GET_TV_SERIES_FOR + site.name for site in
                              bot_user.bot.sites_cinema.all()]
        if cinema_sites_names:
            message_ser = '\n Вы можете выбрать один из сайтов с сериалами: \n'
            message_serials = message_ser + '\n'.join(cinema_sites_names)

        message_news = ''
        news_sites_names = [ALERTING_FOR_NEWS + site.name
                            for site in bot_user.bot.sites_news.iterator()]
        if news_sites_names:
            message_n = '\n Вы можете выбрать один из сайтов с новостями: \n'
            message_news = message_n + '\n'.join(news_sites_names)

        rss = ''
        rss_channels = [ALERTING_FOR_RSS + rss.name
                        for rss in bot_user.bot.rss.iterator()]
        if rss_channels:
            message_rss = '\n Вы можете выбрать один из RSS каналов: \n'
            rss = message_rss + '\n'.join(rss_channels)
        bot_user.send_message(message_serials + message_news + rss)

    @staticmethod
    def siteCinema(bot_user, message):
        command = message['text']
        site_cinema_name = command.split(GET_TV_SERIES_FOR).pop()
        site = models.SiteCinema.objects.filter(name=site_cinema_name, bots=bot_user.bot)
        if site:
            site = site.get()
        else:
            bot_user.send_message('Бот не подписан на "{}"'.format(site_cinema_name))
            return
        message = 'Вы можете подпасаться на следующие сериалы:\n'
        tv_series = [tv_series.name_rus + ' ' + ALERTING_FOR_TV_SERIES + str(tv_series.id)
                     for tv_series in site.tv_series.all()]
        count_tv_series = len(tv_series)
        count_in_page = 40
        if count_tv_series % count_in_page == 0:
            pages = count_tv_series / count_in_page
        else:
            pages = int(count_tv_series / count_in_page) + 1
        for page in range(pages):
            bot_user.send_message(message + '\n'.join(
                tv_series[page * count_in_page:page * count_in_page + count_in_page]))

    @staticmethod
    def tvSeries(bot_user, message):
        command = message['text']
        tv_series_id = command.split(ALERTING_FOR_TV_SERIES).pop()
        tv_series = models.TVSeries.objects.filter(id=tv_series_id)
        if tv_series:
            tv_series = tv_series.get()
            if not tv_series.site.bots.filter(id=bot_user.bot.id):
                bot_user.send_message('Не реально ^^')
                return

            if bot_user.tv_series.filter(tv_series=tv_series):
                bot_user.send_message('Вы уже подписаны на {}\n'.format(
                    tv_series.name_rus))
            else:
                bot_user.tv_series.create(tv_series=tv_series)
                bot_user.send_message('Теперь вы подписаны на {}\n'.format(
                    tv_series.name_rus))
        else:
            bot_user.send_message('Не найдено сериала')

    @staticmethod
    def siteNews(bot_user, message):
        command = message['text']
        site_news_name = command.split(ALERTING_FOR_NEWS).pop()
        news = models.SiteNews.objects.filter(name=site_news_name, bots=bot_user.bot)
        if news:
            news = news.get()
        else:
            bot_user.send_message('Бот не подписан на "{}"'.format(site_news_name))
            return
        if news.users.filter(user=bot_user):
            bot_user.send_message('Вы уже подписаны на новости {}'.format(site_news_name))
        else:
            news.users.create(user=bot_user)  # add relation MtM
            bot_user.send_message('Подписаны на новости {}'.format(site_news_name))

    @staticmethod
    def siteRSS(bot_user, message):
        command = message['text']
        rss_name = command.split(ALERTING_FOR_RSS).pop()
        rss = models.Rss.objects.filter(name=rss_name, bots=bot_user.bot).first()
        # name unique
        if not rss:
            bot_user.send_message('Бот не подписан на канал {}'.format(rss_name))
            return

        _, is_created = bot_user.rss.get_or_create(rss=rss)
        if is_created:
            bot_user.send_message('Подписаны на rss канал {}'.format(rss.url))
        else:
            bot_user.send_message('Вы уже подписаны на rss канал {}'.format(rss.url))

    @staticmethod
    def mySubscriptions(bot_user, message):
        sites_news = [site.site_news.name + '\n' + site.site_news.description for site in
                      bot_user.sites_news.all()]
        my_sites_news = ''
        if sites_news:
            my_sites_news = 'Мои новости :\n' + '\n'.join(sites_news) + '\n'
        sites_tv_series = ['{}'.format(user_tv_series.tv_series) for user_tv_series in
                           bot_user.tv_series.all()]
        my_tv_series = ''
        if sites_tv_series:
            my_tv_series = 'Мои сериалы :\n' + '\n'.join(sites_tv_series)
        if my_tv_series or my_sites_news:
            bot_user.send_message(my_sites_news + my_tv_series)
        else:
            bot_user.send_message('Вы ни на что не подписаны :(  Выберете {}'.format(
                GET_SITES))

    @staticmethod
    def help(bot_user, message):
        bot_user.send_message('''
        Бот позволяет получать информацию о новостях или сериях на которые вы подписаны.
        Для получения просмотра сайтов - выберете {start}
        Если хотите посмотреть на что вы уже подписаны - {subscribe}
        Исходники + просмотр списка ботов на
        https://github.com/Nick1994209/parsing_news_and_send_telegram'''.format(
            start=GET_SITES, subscribe=MY_SUBSCRIPTIONS)
        )

    @staticmethod
    def incorrect_command(bot_user, message):
        bot_user.send_message(
            'Неизвестная команда :-) Выберете команду " {} " для помощи'.format(HELP)
        )
