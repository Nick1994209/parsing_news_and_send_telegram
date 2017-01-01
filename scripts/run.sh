#!/bin/bash


echo 'ACTIVATED django_telegram'
alias django_telegram_managepy="/home/ubuntu/.virtualenvs/django_telegram/bin/python /home/ubuntu/parsing_news_and_send_telegram/manage.py"


django_telegram_managepy parsing_cinema_sites &
django_telegram_managepy parsing_news_sites &
django_telegram_managepy reply_on_telegram_messages &

django_telegram_managepy runserver 0.0.0.0:8000
