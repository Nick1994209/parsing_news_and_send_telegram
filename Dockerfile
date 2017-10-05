FROM python:3

RUN mkdir /ngrok
WORKDIR /ngrok
RUN apt-get update && \
    apt-get install unzip
RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
RUN unzip -o ngrok-stable-linux-amd64.zip
# run ngrok:   /ngrok/ngrok http -hostname localhost 8000

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ENV DJANGO_SETTINGS_MODULE=parsing_news.settings_docker

RUN mkdir /code
WORKDIR /code
ADD ./parsing_news/ /code/
