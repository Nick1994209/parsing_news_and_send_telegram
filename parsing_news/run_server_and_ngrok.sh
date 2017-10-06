#!/usr/bin/env bash

python ./manage.py ngrok --ngrok_command='/ngrok/ngrok' --share_port='8080' &
python ./manage.py runserver 0.0.0.0:8080
