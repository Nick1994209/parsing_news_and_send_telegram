#!/bin/bash

# sudo -u ubuntu -H sh -c "cd ~/$PROJECT && source run_app.sh " &&

workon django_telegram &&

.././manage.py runserver 0.0.0.0:8000 &

.././manage.py parsing_cinema_sites &
.././manage.py parsing_news_sites &
.././manage.py reply_on_telegram_messages &
