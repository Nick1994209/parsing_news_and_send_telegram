# Telegram bot

#### Can use for sites

- animeonline (animeonline_bot)
- pythondigest и simpleisbetterthancomplex (python_news_bot)
- rss (adding rss in admin /admin/core/rss/)

#### How it work

- In /admin/core/telegrambot/ add telegrambot token (https://core.telegram.org/bots#6-botfather)

   and subscribe to sites or rss

- you can subscribe to bot in telegram and choice sites or rss

---

## Work with docker

    docker-compose up

    docker-compose run web python manage.py migrate
    docker-compose run web python manage.py loaddata core/fixtures/site_news.json core/fixtures/site_cinema.json
    docker-compose run web python manage.py createsuperuser

show logs from worked docker

    (web or celery or celery-beat); (celery_1 check, docker ps)
    docker exec -it $(docker ps | grep celery_1 | awk '{print $1}') tail -f /tmp/django_telegram/logs/debug.log
    docker exec -it $(docker ps | grep celery_1 | awk '{print $1}') tail -f /tmp/django_telegram/logs/http_client.log

## Install local (if not docker)

### On server

install requirements.txt
install features

    ./manage.py migrate
    ./manage.py loaddata core/fixtures/site_news.json core/fixtures/site_cinema.json
    
run celery:

    celery -A parsing_news worker --loglevel=info --beat -Q high,normal,low
    celery -A parsing_news beat --loglevel=info
    flower -A parsing_news --port=5555

need install

    sudo apt-get install python-lxml  libxml2  libxml2-dev libxslt-dev
    sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
    (for lxml) - not used    (lxml==3.6.4)


#### if need dump data

    ./manage.py dumpdata core.SiteNews --indent=4 > core/fixtures/sites_news.json
    ./manage.py dumpdata core.SiteCinema --indent=4 > core/fixtures/sites_cinema.json
