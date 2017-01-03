from django.contrib import admin

from . import models

admin.site.register(models.SiteNews)
admin.site.register(models.News)
admin.site.register(models.UserNews)

admin.site.register(models.SiteCinema)
admin.site.register(models.TVSeries)
admin.site.register(models.Series)

admin.site.register(models.UserSeries)

admin.site.register(models.TelegramBot)
admin.site.register(models.TelegramUser)
