import datetime
import requests
from bs4 import BeautifulSoup
import re


class HH_python:
    """
    https://hh.ru/search/vacancy?salary=60000&only_with_salary=true&area=1&enable_snippets=true&schedule=fullDay&text=python&clusters=true&employment=full&experience=between1And3&from=cluster_experience

    from 60k - 80k ruble
    """
    SITE_URL = 'https://hh.ru'

    @classmethod
    def get_all_news(cls, page=1):
        if page > 1:
            return []

        rss = '/search/vacancy/rss'
        from_salary = 60  # k
        params = "?salary={from_salary}".format(from_salary=from_salary)\
               + "&only_with_salary=true&area=1&"\
               +"enable_snippets=true" \
               + "&schedule=fullDay&experience=between1And3"\
               +"&text=python&clusters=true&employment=full"

        URL = cls.SITE_URL + rss + params

        response = requests.get(URL)
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
