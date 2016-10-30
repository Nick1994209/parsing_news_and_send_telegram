## БОТ для телеграма

#### Сейчас доступен для сайта http://animeonline.su/
#### animeonline_bot  

Бот позволяет получать последние вышедшие сериалы, аниме



### On server

on server install virtualenvwrapper
sudo apt-get install python-lxml

create env with name "django_telegram"

install requirements.txt
install features
    ./manage.py migrate
    ./manage.py loaddata cinema_sites news_sites

for run all need run script in scripts

    source scripts/run.sh
    
    source run.sh & disown      (if need run )

    
