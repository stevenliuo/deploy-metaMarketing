FROM python:3.11-slim

RUN apt-get update && apt-get -y upgrade && pip install --upgrade pip

RUN mkdir /web_app

WORKDIR /web_app

COPY requirements.txt /web_app

RUN pip install -r requirements.txt && rm -rf /root/.cache/pip

COPY . /web_app

ENV ENV_FILE=/web_app/.env

RUN celery --app server worker -Q openai,mail_notification,ppt_task_creator -c 5 --loglevel=info
