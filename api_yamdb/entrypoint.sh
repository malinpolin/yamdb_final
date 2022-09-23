#!/bin/bash
python manage.py migrate --noinput && \
python manage.py collectstatic --no-input && \
python manage.py createsuperuser --username malinpolin --no-input && \
gunicorn api_yamdb.wsgi:application --bind 0:8000
