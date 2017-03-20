from django.contrib import admin

from . import models


def inline(model, can_delete=False, show_change_link=True):
    class NewInline(admin.TabularInline):
        extra = 0
    NewInline.model = model
    NewInline.can_delete = can_delete
    NewInline.show_change_link = show_change_link
    # NewInline.show_change_link = readonly_fields
    return NewInline


def create_admin_class(inlines):
    class NewAdminClass(admin.ModelAdmin):
        pass
    NewAdminClass.inlines = inlines
    return NewAdminClass


# ---------- RSS --------------
admin.site.register(models.Rss, create_admin_class(inlines=[inline(models.RssNews)]))
admin.site.register(models.RssNews)

# ----------- NEWS ----------------
admin.site.register(models.SiteNews, create_admin_class(inlines=[inline(models.News)]))
admin.site.register(models.News)


# ----------- CINEMA ---------------
admin.site.register(models.SiteCinema, create_admin_class(inlines=[inline(models.TVSeries)]))
admin.site.register(models.TVSeries, create_admin_class(inlines=[inline(models.Series)]))
admin.site.register(models.Series)


# ------------ BOT ------------------
admin.site.register(models.TelegramBot, create_admin_class(
    inlines=[inline(models.TelegramUser, can_delete=True)]
))
telegram_user_inlines = [inline(models.UserRss), inline(models.UserSeries), inline(models.UserNews)]
admin.site.register(models.TelegramUser, create_admin_class(telegram_user_inlines))
