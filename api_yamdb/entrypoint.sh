#!/bin/bash
python manage.py migrate --noinput && \
python manage.py collectstatic --no-input && \
python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL && \
gunicorn api_yamdb.wsgi:application --bind 0:8000
