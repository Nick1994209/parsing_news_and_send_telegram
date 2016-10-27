import requests
from bs4 import BeautifulSoup
import re


URL = 'http://animeonline.su/ongoing/'
response = requests.get(URL)

content = BeautifulSoup(response.content, 'html.parser')
div_with_anime = content.find(id='dle-content')
divs_with_anime = div_with_anime.find_all('div', {"class" : "new_" })
print(len(divs_with_anime))

example = 'Проект-Б'

for anime_div in divs_with_anime:
    label_rus = anime_div.find_all('span', {"class" : "label_rus" })
    # print(label_rus)
    if [True for label in label_rus if re.search(example, label.decode_contents())]:
        print('Find Project-B')