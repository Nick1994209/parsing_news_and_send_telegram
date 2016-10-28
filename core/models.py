from django.db import models
from sites import AllSites
from telegram import Bot


class Site(models.Model):
    url = models.URLField(verbose_name='Site address')
    name = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_all_sites(cls, command):
        sites = [command+site.name for site in cls.objects.all()]
        return '\n'.join(sites)

    def save(self, **kwargs):
        if hasattr(AllSites, self.name):
            return super().save()
        else:
            raise Exception('Site not in [{}]'.format(AllSites.all_sites()))

    def update_series(self):
        series = AllSites.get_all_series(self.name)

    def get_new_episodes(self):
        page = 1

        while True:
            episodes = AllSites.get_all_series(self.name, page)
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

                    message1 = 'Для {} вышла новая серия \n'.format(tv_series.__str__())
                    message2 = '{}\n'.format(series.__str__())
                    tv_series.users_send_message(message1 + message2)

            if next_page:
                page += 1
            else:
                break

    def get_new_tv_series_with_episodes(self):
        page = 1
        while True:
            episodes = AllSites.get_all_series(self.name, page)
            if not episodes: break

            existed_serieses = []
            for episode in episodes:
                if self.tv_series.filter(name_rus=episode['name_rus']).exists():
                    continue

                tv_series = self.tv_series.create(
                    name_rus=episode.get('name_rus', ''), name_eng=episode.get('name_eng', ''))

                tv_series.series.create(
                    number=episode.get('number', '1'), url=episode.get('url', ''))
            page += 1

    def __str__(self):
        return self.name


class SiteTVSeries(models.Model):
    site = models.ForeignKey(Site, related_name='tv_series')
    name_rus = models.CharField(max_length=255, blank=True)
    name_eng = models.CharField(max_length=255, blank=True)

    def users_send_message(self, message):
        for user in self.users.all():
            user.user.send_message(message)

    def __str__(self):
        return '%s %s site=%s' % (self.name_rus, self.name_eng, self.site)


class Series(models.Model):
    tv_series = models.ForeignKey(SiteTVSeries, related_name='series')
    number = models.FloatField(models.Model, default=1)
    url = models.URLField(blank=True)

    class Meta:
        unique_together = 'tv_series', 'number'

    def __str__(self):
        return '{} {}'.format(self.number, self.tv_series)

    # def save(self, **kwargs):
    #     object = super().save(**kwargs)
    #     self.users_alert()
    #     return object
    #
    # def users_alert(self):
    #     message = 'Серия={} Урл={} Название={}'.format(self.number, self.url, self.tv_series.name_rus)
    #     if self.tv_series.users.all().exists():
    #         for user in self.tv_series.users.all():
    #             user.user.send_message(message)


class TelegramBot(models.Model):
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, help_text='Set in save')
    username = models.CharField(max_length=255, blank=True) # set in save
    last_message_id = models.IntegerField(default=0)

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
        return super().save(**kwargs)

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
    tv_series = models.ForeignKey(SiteTVSeries, related_name='users')
    dc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{user} {serial}'.format(user=self.user, serial=self.serial)
