from sites.anime import animeonline
from sites.news import pythondigest


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


class AllSitesNews(General):
    # python
    pythondigest = pythondigest

    @classmethod
    def get_all_news(cls, site_name, page=1):

        site = getattr(cls, site_name, None)
        if site:
            return site.get_all_news(page)
        else:
            raise Exception("Site don't parsing")
