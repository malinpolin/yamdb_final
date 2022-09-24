#!/bin/bash
python manage.py migrate --noinput && \
python manage.py collectstatic --no-input && \
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi
cp /static/redoc.yaml /app/static
gunicorn api_yamdb.wsgi:application --bind 0:8000
