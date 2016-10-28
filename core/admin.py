from django.contrib import admin
from . import models


admin.site.register(models.Site)
admin.site.register(models.SiteTVSeries)
admin.site.register(models.Series)

admin.site.register(models.UserSeries)

admin.site.register(models.TelegramBot)
admin.site.register(models.TelegramUser)
