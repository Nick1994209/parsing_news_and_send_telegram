from sites import animeonline


class AllSites(object):
    animeonline = animeonline

    @classmethod
    def get_all_series(cls, site_name, page=1):

        site = getattr(cls, site_name, None)
        if site:
            return site.get_all_episodes(page)
        else:
            raise Exception('Site dont parsing')

    @classmethod
    def all_sites(cls):
        sites = []
        for attr in dir(cls):
            if '__' in attr:
                continue
            if not callable(getattr(cls, attr)):
                sites.append(attr)
        return ', '.join(sites)
