import feedparser
import requests

url = 'https://pythondigest.ru/rss/'


def rss_parser(url):
    response = requests.get(url)
    pars = feedparser.parse(response.content)
    return pars.get('entries') or []
