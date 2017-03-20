import feedparser
from utils.http_client import simple_client


def rss_parser(url):
    response = simple_client.get(url)
    pars = feedparser.parse(response.content)
    return pars.get('entries') or []
