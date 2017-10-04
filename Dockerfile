FROM python:3

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ENV DJANGO_SETTINGS_MODULE=parsing_news.settings_docker

RUN mkdir /code
WORKDIR /code
ADD ./parsing_news/ /code/
