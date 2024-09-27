#!/bin/bash

python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec gunicorn server.wsgi:application -c gunicorn.py --reload