class General(object):
    @classmethod
    def all_sites(cls):
        sites = []
        for attr in dir(cls):
            if '__' in attr:
                continue
            if not callable(getattr(cls, attr)):
                sites.append(attr)
        return ', '.join(sites)


from sites.anime import animeonline


class AllSitesCinema(General):
    # anime
    animeonline = anime.animeonline

    @classmethod
    def get_all_series(cls, site_name, page=1):

        site = getattr(cls, site_name, None)
        if site:
            return site.get_all_episodes(page)
        else:
            raise Exception("Site don't parsing")


from sites.news.python import pythondigest
from sites.news.python import simpleisbetterthancomplex # python/django


class AllSitesNews(General):
    # python
    pythondigest = pythondigest
    simpleisbetterthancomplex = simpleisbetterthancomplex

    @classmethod
    def get_all_news(cls, site_name, page=1):

        site = getattr(cls, site_name, None)
        if site:
            return site.get_all_news(page)
        else:
            raise Exception("Site don't parsing")
