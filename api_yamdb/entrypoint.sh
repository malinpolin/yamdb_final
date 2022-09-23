#!/bin/bash
python manage.py migrate --noinput && \
python manage.py collectstatic --no-input && \
source '.env' && python manage.py createsuperuser --no-input && \
gunicorn api_yamdb.wsgi:application --bind 0:8000
