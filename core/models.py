from django.utils import timezone
from django.db import models
from sites import AllSitesCinema, AllSitesNews
from telegram import Bot


class Site(models.Model):
    url = models.URLField(verbose_name='Site address')
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=60, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
        
        
class SiteNews(Site):
    def save(self, **kwargs):
        if hasattr(AllSitesNews, self.name):
            return super().save()
        else:
            raise Exception('Site not in news [{}]'.format(AllSitesNews.all_sites()))

    def users_send_message(self, message):
        for user in self.users.all():
            user.user.send_message(message)

    def get_news(self):
        page = 1

        all_page_news = AllSitesNews.get_all_news(self.name, page)

        for news_data in all_page_news:
            news_obj = self.news.filter(**news_data)
            if news_obj:
                continue
            else:
                news_obj = self.news.create(**news_data)

                message1 = 'На сайте "{}" \n'.format(self.name)
                message2 = '---"{}  {}" --- \n'.format(news_obj.name_rus, news_obj.name_eng)
                message3 = '{}\n'.format(news_obj.description)
                message4 = '{}\n'.format(news_obj.url if news_obj.url else '')

                self.users_send_message(message1 + message2 + message3 + message4)


class News(models.Model):
    site = models.ForeignKey(SiteNews, related_name='news')

    url = models.URLField(blank=True)
    tags = models.TextField(blank=True)
    description = models.TextField(blank=True)
    name_rus = models.CharField(max_length=255, blank=True)
    name_eng = models.CharField(max_length=255, blank=True)
    number = models.FloatField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = '-date_created',

    def __str__(self):
        name = self.name_rus if self.name_rus else self.name_eng
        return name + ' site={}'.format(self.site)


class SiteCinema(Site):

    def save(self, **kwargs):
        if hasattr(AllSitesCinema, self.name):
            return super().save()
        else:
            raise Exception('Site not in [{}]'.format(AllSitesCinema.all_sites()))

    def get_new_episodes(self):
        page = 1
        max_count_page = 4

        while True:
            if page > max_count_page: break
            episodes = AllSitesCinema.get_all_series(self.name, page)
            if not episodes: break

            next_page = True

            for episode in episodes:
                tv_series = self.tv_series.filter(name_rus=episode['name_rus'])
                if tv_series:
                    tv_series = tv_series.get()
                else:
                    tv_series = self.tv_series.create(
                        name_rus=episode.get('name_rus', ''),
                        name_eng=episode.get('name_eng', ''))

                number = number=episode.get('number', '1')
                series = tv_series.series.filter(number__gte=number)
                if series:
                    next_page = False
                else:
                    series = tv_series.series.create(
                        number=number,
                        url=episode.get('url', ''))

                    tv_series.date_release_last_ongoing_series = timezone.now()
                    tv_series.save()

                    message1 = 'На сайте "{}" \n'.format(tv_series.site.name)
                    message2 = ' "{}" ({})\n'.format(tv_series.name_rus, tv_series.name_eng)
                    message3 = 'Вышла новая серия {} {}'.format(series.number, series.url)
                    tv_series.users_send_message(message1 + message2 + message3)

            if next_page:
                page += 1
            else:
                break


class TVSeries(models.Model):
    site = models.ForeignKey(SiteCinema, related_name='tv_series')
    name_rus = models.CharField(max_length=255, blank=True)
    name_eng = models.CharField(max_length=255, blank=True)

    date_release_last_ongoing_series = models.DateTimeField(default=timezone.now)

    def users_send_message(self, message):
        for user in self.users.all():
            user.user.send_message(message)

    class Meta:
        ordering = '-date_release_last_ongoing_series',

    def __str__(self):
        return '%s %s site=%s' % (self.name_rus, self.name_eng, self.site)


class Series(models.Model):
    tv_series = models.ForeignKey(TVSeries, related_name='series')
    number = models.FloatField(models.Model, default=1)
    url = models.URLField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = 'tv_series', 'number'
        ordering = '-date_created',

    def __str__(self):
        return '{} {}'.format(self.number, self.tv_series)


class TelegramBot(models.Model):
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, help_text='Set from telegram.api get_me')
    username = models.CharField(max_length=255, blank=True, help_text='Set from telegram.api get_me') # set in save
    last_message_id = models.IntegerField(default=0)

    sites_cinema = models.ManyToManyField(SiteCinema, related_name='bots', blank=True)
    sites_news = models.ManyToManyField(SiteNews, related_name='bots', blank=True)

    def get_bot(self):
        return Bot(self.token)

    def get_last_messages(self):
        messages = self.get_bot().get_new_messages(self.last_message_id)
        if messages:
            self.last_message_id = messages[-1]['message_id']
            self.save()
        return messages

    def save(self, **kwargs):
        about_bot = self.get_bot().get_me()
        if about_bot['ok']:
            if not hasattr(self, 'username') or not self.username:
                self.username = about_bot['result']['username']
            if not hasattr(self, 'name') or not self.name:
                self.name = about_bot['result']['first_name']
        if self.id:
            self.clear_users_relation_with_unsubscribing_sites()

        return super().save(**kwargs)

    def clear_users_relation_with_unsubscribing_sites(self):
        'if relation with sites is closed need delete relations bot_users with sites'
        users_id = [user.id for user in self.users.all()]

        # sites_news
        subscribe_on_sites_news = [site.id for site in self.sites_news.all()]
        UserNews.objects.filter(user__in=users_id).exclude(site_news__in=subscribe_on_sites_news).delete()

        # sites_cinema
        subscribe_on_sites_cinema = [site.id for site in self.sites_cinema.all()]
        UserSeries.objects.filter(user__in=users_id).exclude(tv_series__site__in=subscribe_on_sites_cinema).delete()

    def __str__(self):
        return self.name

    def users_send_message(self, message):
        bot = self.get_bot()

        for user in self.users.all():
            bot.send_message(user.user_id, message)


class TelegramUser(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    bot = models.ForeignKey(TelegramBot, related_name='users')

    class Meta:
        unique_together = 'user_id', 'bot'

    def send_message(self, message):
        bot = self.bot.get_bot()
        bot.send_message(self.user_id, message)

    def __str__(self):
        return '{user_id} {username} bot={bot}'.format(user_id=self.user_id, username=self.username, bot=self.bot.username)


class UserSeries(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='tv_series')
    tv_series = models.ForeignKey(TVSeries, related_name='users')
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if self.tv_series.site.bots.filter(id=self.user.bot.id):
            return super().save(**kwargs)

    def __str__(self):
        return '{user} {tv_series}'.format(user=self.user, tv_series=self.tv_series)

    class Meta:
        unique_together = ('user', 'tv_series')


class UserNews(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='sites_news')
    site_news = models.ForeignKey(SiteNews, related_name='users')
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if self.site_news.bots.filter(id=self.user.bot.id):
            return super().save(**kwargs)

    def __str__(self):
        return '{user} {news}'.format(user=self.user, news=self.site_news)

    class Meta:
        unique_together = ('user', 'site_news')
