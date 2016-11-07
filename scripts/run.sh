#!/bin/bash


workon django_telegram;


.././manage.py parsing_cinema_sites &
.././manage.py parsing_news_sites &
.././manage.py reply_on_telegram_messages &

.././manage.py runserver 0.0.0.0:8000 &
