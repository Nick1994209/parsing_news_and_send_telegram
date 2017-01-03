## БОТ для телеграма

#### Сейчас доступен для сайтов:
##### animeonline  pythondigest   simpleisbetterthancomplex
#### animeonline_bot  

Бот позволяет получать последние вышедшие сериалы, аниме

#### python_news_bot

Этот бот позволяет получать последние статьи с python/django 
(есть возможность выбора источника подписки)


### On server

on server install virtualenvwrapper


create env with name "django_telegram"

install requirements.txt
install features
    ./manage.py migrate
    ./manage.py loaddata core/fixtures/site_news.json core/fixtures/site_cinema.json

for run all need run script in scripts

    source scripts/run.sh
    
    source run.sh & disown      (if need run )

    

############################################# 
sudo apt-get install python-lxml  libxml2  libxml2-dev libxslt-dev
sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
(for lxml) - not used    (lxml==3.6.4)


#### dump data
./manage.py dumpdata core.SiteNews --indent=4 > core/fixtures/sites_news.json
./manage.py dumpdata core.SiteCinema --indent=4 > core/fixtures/sites_cinema.json