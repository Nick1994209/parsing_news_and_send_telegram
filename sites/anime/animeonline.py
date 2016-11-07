import requests
from bs4 import BeautifulSoup
import re

SITE_URL = 'http://animeonline.su'


def get_all_episodes(page=1): # RSS
    URL = SITE_URL + '/zend/episodes.xml'
    if page > 2:
        return []

    response = requests.get(URL)

    content_bs = BeautifulSoup(response.content, 'html.parser')
    anime_items_bs = content_bs.find_all('item')

    anime_values = []
    for item_bs in anime_items_bs:
        episode = {}
        tv_series = {}

        row_name = item_bs.find('title').getText()

        begin_str, end_str = '[!\[CDATA\[', '(\]\]'
        regular_rm_CDATA = '[({begin_str}),({end_str})]'.format(begin_str=begin_str, end_str=end_str)

        tv_series['name_rus'] = re.sub(regular_rm_CDATA, '', row_name)

        episode['url'] = item_bs.find('link').getText()

        description_row1 = re.sub(regular_rm_CDATA, '', item_bs.find('description').getText())
        description_row2 = re.sub('<img(.*)>', '', description_row1)
        description_row3 = re.sub('Эпизод # ', '', description_row2)

        number = description_row3.split(' ')[0]

        episode['number'] = number
        episode['description'] = description_row3

        anime_values.append({'episode': episode, 'tv_series': tv_series})

    return anime_values


def get_all_episodes_NOT_RSS(page=1): #
    URL = SITE_URL + '/ongoing/'

    response = requests.get(URL + 'page/{}'.format(page))

    content_bs = BeautifulSoup(response.content, 'html.parser')
    block_anime_bs = content_bs.find(id='content').find(id='dle-content')
    anime_divs = block_anime_bs.find_all('div', {"class": "new_"})

    anime_values = []
    for anime_div_bs in anime_divs:
        episode = {}
        episode['name_rus'] = anime_div_bs.find('span', {"class": "label_rus"}).decode_contents()
        episode['name_eng'] = anime_div_bs.find('span', {"class": "label_eng"}).decode_contents()

        for href_bs in anime_div_bs.find_all('a'):
            if '!/episode/' in href_bs['href']:
                episode_href = href_bs['href']
                episode['url'] = SITE_URL + episode_href

            href_html = href_bs.decode_contents()
            if 'эпизод' in href_html:
                if re.findall('\d+', href_html):
                    episode_number = int(re.findall('\d+', href_html)[0])
                    episode['number'] = episode_number

        anime_values.append(episode)

    return anime_values


def example():
    URL = 'http://animeonline.su/ongoing/'
    response = requests.get(URL)

    content = BeautifulSoup(response.content, 'html.parser')
    div_with_anime = content.find(id='dle-content')
    divs_anime = div_with_anime.find_all('div', {"class": "new_"})
    print(len(divs_anime))

    example = 'Проект-Б'

    for anime_div in divs_anime:
        label_rus = anime_div.find_all('span', {"class": "label_rus"})
        # print(label_rus)
        if [True for label in label_rus if
            re.search(example, label.decode_contents())]:
            print('Find Project-B')
            print(label_rus)