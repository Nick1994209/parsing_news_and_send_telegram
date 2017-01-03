import datetime
import re

import requests
from bs4 import BeautifulSoup


class HH_python:
    """
    https://hh.ru/search/vacancy?salary=60000&only_with_salary=true&area=1&enable_snippets=true&schedule=fullDay&text=python&clusters=true&employment=full&experience=between1And3&from=cluster_experience

    from 60k + k ruble
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

        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'User-Agent': '',
            'Content-Type': 'application/rss+xml;charset=UTF-8'
        }

        response = requests.get(URL, headers=headers)
        content_bs = BeautifulSoup(response.text, 'html.parser')

        block_vacations_bs = content_bs.find('channel')
        all_vacations = block_vacations_bs.find_all('item')

        news_values = []
        for vacation_bs in all_vacations:
            vacation = {}

            vacation['name_rus'] = vacation_bs.find('title').decode_contents()
            vacation['date'] = cls.parse_date(vacation_bs.find('pubdate').decode_contents())
            vacation['description'] = cls.parse_description(vacation_bs.find('description').decode_contents())
            vacation['url'] = vacation_bs.find('guid').decode_contents()

            news_values.append(vacation)
        return news_values

    @staticmethod
    def parse_date(raw_date):
        regular_search_date, strp_date = '\d+-\d+-\d+', '%Y-%M-%d'
        date_str = re.findall(regular_search_date, raw_date).pop()
        return datetime.datetime.strptime(date_str, strp_date).date()

    @staticmethod
    def parse_description(raw_description):
        print(raw_description)
        regular_search = r'<!\[CDATA\[\n(.*)\n\]\]>'  # instead \n need re.MULTILINE
        description_raw2 = re.findall(regular_search, raw_description).pop()
        description = description_raw2.replace('<p>', '\n')
        description = description.replace('</p>', '')
        return description


print(HH_python.get_all_news())
