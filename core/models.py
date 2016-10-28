from django.db import models


class Site(models.Model):
    url = models.URLField(verbose_name='Site address')


class SiteTVSeries(models.Model):
    site = models.ForeignKey(Site, related_name='tv_series')
    name = models.CharField(max_length=255, verbose_name="Название сериала")


class Series(models.Model):
    tv_series = models.ForeignKey(SiteTVSeries, related_name='series')
    number_series = models.FloatField(models.Model, default=1)
    url = models.URLField()


class TelegramUser(models.Model):
    id = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)


class UserSeries(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='series')
    serial = models.ForeignKey(SiteTVSeries, related_name='users')
    dc = models.DateTimeField(auto_now_add=True)
