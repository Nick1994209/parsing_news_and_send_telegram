import datetime

import logging
from django.utils import timezone

from core import models

logger = logging.getLogger('tasks')


def parsing_cinema(*args, **kwargs):
    parsing_and_sending()
    delete_old_tv_series()


def parsing_and_sending():
    for site in models.SiteCinema.objects.filter(bots__users__isnull=False).distinct():
        new_episodes = []
        # try:
        new_episodes = site.get_new_episodes()
        # except Exception as e:
        #     print('exception! cinema_sites: ' + str(e))
        #     logger.warning(str(e), 'parsing_cinema_sites.log')

        for episode in new_episodes:
            new_episode_send_message(episode)


def new_episode_send_message(episode):
        message = """На сайте "{site_name}"
        {tv_series_name}
        Вышла новая серия {number} {url}
        {description}
        """.format(
            site_name=episode.tv_series.site.name,
            tv_series_name=episode.tv_series.name_rus,
            number=episode.number, url=episode.url,
            description=episode.description
        )
        episode.tv_series.users_send_message(message)


def delete_old_tv_series():
    now = timezone.now()
    month_ago = now - datetime.timedelta(days=30)
    models.TVSeries.objects.filter(date_release_last_ongoing_series__lte=month_ago) \
        .delete()
