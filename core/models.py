from django.db import models


class Site(models.Model):
    url = models.URLField(verbose_name='Адрес')


class SiteSeries(models.Model):
    site = models.ForeignKey(Site, related_name='series')
    url = models.URLField(verbose_name='Урл выбора сайта')


class TelegramUser(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)


class UserSeries(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='series')
    serial = models.ForeignKey(SiteSeries, related_name='users')
    dc = models.DateTimeField(auto_now_add=True)
