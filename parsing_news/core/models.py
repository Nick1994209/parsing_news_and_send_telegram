import logging
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from utils.tools import prepare_list_dict
from sites import AllSitesCinema, AllSitesNews, rss_parser
from telegram import Bot as TelegramBotApi

logger = logging.getLogger(__name__)


class Site(models.Model):
    url = models.URLField(verbose_name='Site address')
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=60, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Rss(Site):
    def get_news(self):
        parsed_channel = rss_parser(self.url)
        new_rss_news = []
        for parsed_news in parsed_channel:
            rss_news, is_created = self.news.get_or_create(
                title=parsed_news.get('title', '').strip(),
                url=parsed_news.get('link', '').strip(),
                description=self.get_description(parsed_news).strip()
            )
            if is_created:
                new_rss_news.append(rss_news)
        return new_rss_news

    def users_send_message(self, message):
        for user in self.users.all():
            user.user.send_message(message)

    @staticmethod
    def get_description(news):
        if news.get('summary') and isinstance(news.get('summary'), str):
            return news.get('summary')
        if news.get('summary_detail') and isinstance(news.get('summary_detail'), str):
            return news.get('summary_detail')
        return ''


class RssNews(models.Model):
    rss = models.ForeignKey(Rss, related_name='news', on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

        
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
        all_page_news = AllSitesNews.get_all_news(self.name)

        if not all_page_news:
            return

        all_page_news = prepare_list_dict(all_page_news)
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
    site = models.ForeignKey(SiteNews, related_name='news', on_delete=models.CASCADE)

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
        new_episodes = []

        while True:
            if page > max_count_page: break
            page_series = AllSitesCinema.get_all_series(self.name, page)
            if not page_series: break

            page_series.reverse()  # from last to new series
            page_series = prepare_list_dict(page_series)

            next_page = True

            for series in page_series:
                about_tv_series = series['tv_series']
                about_episode = series['episode']
                tv_series, _ = self.tv_series.get_or_create(**about_tv_series)

                episode_number = about_episode.get('number', '1')
                is_episodes_exists = tv_series.series.filter(number__gte=episode_number).exists()
                if is_episodes_exists:
                    next_page = False
                else:
                    episode = tv_series.series.create(**about_episode)
                    new_episodes.append(episode)
                    tv_series.date_release_last_ongoing_series = timezone.now()
                    tv_series.save()

            if next_page:
                page += 1
            else:
                break
        return new_episodes


class TVSeries(models.Model):
    site = models.ForeignKey(SiteCinema, related_name='tv_series', on_delete=models.CASCADE)
    name_rus = models.CharField(max_length=255, blank=True)
    name_eng = models.CharField(max_length=255, blank=True)

    date_release_last_ongoing_series = models.DateTimeField(default=timezone.now)

    def users_send_message(self, message):
        for user in self.users.all():
            user.user.send_message(message)

    class Meta:
        ordering = 'date_release_last_ongoing_series',

    def __str__(self):
        return '%s %s site=%s' % (self.name_rus, self.name_eng, self.site)


class Series(models.Model):
    tv_series = models.ForeignKey(TVSeries, related_name='series', on_delete=models.CASCADE)
    number = models.FloatField(models.Model, default=1)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = 'tv_series', 'number'
        ordering = '-date_created',

    def __str__(self):
        return '{} {}'.format(self.number, self.tv_series)


class TelegramBot(models.Model):
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, help_text='From telegram.api get_me')
    username = models.CharField(max_length=255, blank=True, help_text='From telegram.api get_me')
    last_message_id = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    sites_cinema = models.ManyToManyField(SiteCinema, related_name='bots', blank=True)
    sites_news = models.ManyToManyField(SiteNews, related_name='bots', blank=True)
    rss = models.ManyToManyField(Rss, related_name='bots', blank=True)

    def get_bot(self):
        return TelegramBotApi(self.token)

    def get_last_messages(self):
        messages = self.get_bot().get_new_messages(self.last_message_id)
        if messages:
            self.last_message_id = messages[-1]['message_id']
            self.save()
        return messages

    def save(self, **kwargs):
        about_bot = self.get_bot().get_me()
        if about_bot.get('ok'):
            if not hasattr(self, 'username') or not self.username:
                self.username = about_bot['result']['username']
            if not hasattr(self, 'name') or not self.name:
                self.name = about_bot['result']['first_name']
        else:
            self.is_active = False
            raise ValidationError('Бот не подтвержден или удален')
        if self.id:
            self.clear_users_relation_with_unsubscribing_sites()
        return super().save(**kwargs)

    def clear_users_relation_with_unsubscribing_sites(self):
        'if relation with sites is closed need delete relations bot_users with sites'
        users_id = [user.id for user in self.users.all()]

        # sites_news
        subscribe_on_sites_news = self.sites_news.values_list('id', flat=True)
        # [site.id for site in self.sites_news.all()]
        (UserNews.objects
         .filter(user__in=users_id)
         .exclude(site_news__in=subscribe_on_sites_news)
         .delete())

        # sites_cinema
        # subscribe_on_sites_cinema = [site.id for site in self.sites_cinema.all()]
        subscribe_on_sites_cinema = self.sites_cinema.values_list('id', flat=True)
        (UserSeries.objects
         .filter(user__in=users_id)
         .exclude(tv_series__site__in=subscribe_on_sites_cinema)
         .delete())

    def __str__(self):
        return self.name

    def users_send_message(self, message):
        bot = self.get_bot()

        for user_id in self.users.values_list('user_id', flat=True):
            bot.send_message(user_id, message)


class TelegramUser(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    bot = models.ForeignKey(TelegramBot, related_name='users', on_delete=models.CASCADE)

    class Meta:
        unique_together = 'user_id', 'bot'

    def send_message(self, message):
        bot = self.bot.get_bot()
        response = bot.send_message(self.user_id, message)

        return response

    def check_response(self, response):
        if response.status_code == 403:
            logger.info('TelegramUser {} unsubscribe from TelegramBot {}'.format(
                self.username, self.bot.username))
            self.is_active = False
            self.save()
        elif response.status_code == 200 and self.is_active == False:
            self.is_active = True
            self.save()

    def __str__(self):
        return '{user_id} {username} bot={bot}'.format(
            user_id=self.user_id,
            username=self.username,
            bot=self.bot.username
        )


class UserRss(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='rss', on_delete=models.CASCADE)
    rss = models.ForeignKey(Rss, related_name='users', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if self.rss.bots.filter(id=self.user.bot.id):
            return super().save(**kwargs)

    class Meta:
        unique_together = ('user', 'rss')


class UserSeries(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='tv_series', on_delete=models.CASCADE)
    tv_series = models.ForeignKey(TVSeries, related_name='users', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if self.tv_series.site.bots.filter(id=self.user.bot.id):
            return super().save(**kwargs)

    def __str__(self):
        return '{user} {tv_series}'.format(user=self.user, tv_series=self.tv_series)

    class Meta:
        unique_together = ('user', 'tv_series')


class UserNews(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='sites_news', on_delete=models.CASCADE)
    site_news = models.ForeignKey(SiteNews, related_name='users', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if self.site_news.bots.filter(id=self.user.bot.id):
            return super().save(**kwargs)

    def __str__(self):
        return '{user} {news}'.format(user=self.user, news=self.site_news)

    class Meta:
        unique_together = ('user', 'site_news')
