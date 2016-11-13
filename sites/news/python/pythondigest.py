import datetime
import requests
from bs4 import BeautifulSoup
import re


class Pythondigest:
    SITE_URL = 'https://pythondigest.ru'

    @classmethod
    def get_all_news(cls, page=1):
        URL = cls.SITE_URL + '/feed/'

        response = requests.get(URL + '?page/{}'.format(page))
        content_bs = BeautifulSoup(response.content, 'html.parser')

        block_all_news_bs = content_bs.find('div', {'class': 'news-list'})
        all_news = block_all_news_bs.find_all('div', {'class': 'item-container'})

        news_values = []
        for news_bs in all_news:
            news = {}

            # get datetime and get description
            element_with_datetime_and_description_bs = news_bs.find('div', {'class': 'news-line-dates'})
            regular_search_date = '\d+\.\d+\.\d+'
            date_str = re.findall(regular_search_date, element_with_datetime_and_description_bs.decode_contents()).pop()
            news['date'] = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
            news['description'] = element_with_datetime_and_description_bs.find('a').decode_contents()

            news['url'] = news_bs.find('h4').find('a')['href']
            news['name_rus'] = news_bs.find('h4').find('a').decode_contents()

            news_values.append(news)
        return news_values
