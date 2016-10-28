import requests
from bs4 import BeautifulSoup
import re


URL = 'http://animeonline.su/ongoing/'


def get_all_episodes(page=1):
    response = requests.get(URL + 'page/{}'.format(page))

    content_bs = BeautifulSoup(response.content, 'html.parser') # response.content - находится весь html код страницы
    block_anime_bs = content_bs.find(id='content').find(id='dle-content')
    anime_divs_bs = block_anime_bs.find_all('div', {"class": "new_"})

    anime_values = []
    for anime_div_bs in anime_divs_bs:
        episod = {}
        episod['name_rus'] = anime_div_bs.find('span', {"class": "label_rus"}).decode_contents()
        episod['name_eng'] = anime_div_bs.find('span', {"class": "label_eng"}).decode_contents()

        for href_bs in anime_div_bs.find_all('a'):
            if '!/episode/' in href_bs['href']:
                episod_href = href_bs['href']
                episod['url'] = episod_href

            href_html = href_bs.decode_contents()
            if 'эпизод' in href_html:
                if re.findall('\d+', href_html):
                    episod_number = int(re.findall('\d+', href_html)[0])
                    episod['number'] = episod_number

        anime_values.append(episod)

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