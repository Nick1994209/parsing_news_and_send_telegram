import datetime
import requests
from bs4 import BeautifulSoup
import re
import urllib

SITE_URL = 'https://simpleisbetterthancomplex.com/'


def get_all_news(page=1):
    if page == 1:
        URL = SITE_URL + 'feed.xml'
    else:
        return []

    response = requests.get(URL)
    content_bs = BeautifulSoup(response.content, 'lxml')

    all_news = content_bs.find_all('item')

    news_values = []
    for news_bs in all_news:
        news = {}

        news['name_eng'] = news_bs.find('title').getText()
        news['url'] = news_bs.find('guid').getText()
        news['tags'] = ', '.join([tag.getText() for tag in news_bs.find_all('category')])

        big_description = news_bs.find('description').getText()
        description_bs = BeautifulSoup(big_description, 'html.parser')
        news['description'] = description_bs.find('p').getText()

        # regular_search_date = '\d+\.\d+\.\d+'
        # news['dc'] = datetime.datetime.strptime(date_str, '%d.%m.%Y')

        news_values.append(news)

    return news_values
