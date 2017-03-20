#!/bin/bash


echo 'ACTIVATED django_telegram';
alias current_python="/home/ubuntu/.virtualenvs/django_telegram/bin/python"
alias django_telegram_managepy="current_python /home/ubuntu/parsing_news_and_send_telegram/parsing_news/manage.py"

django_telegram_managepy parsing_cinema &
django_telegram_managepy parsing_news &
django_telegram_managepy parsing_rss &
django_telegram_managepy reply_on_telegram_messages &

django_telegram_managepy runserver 0.0.0.0:8000