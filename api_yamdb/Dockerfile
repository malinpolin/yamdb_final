FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

RUN python manage.py migrate --noinput

RUN python manage.py collectstatic --no-input 

RUN python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL

COPY static/redoc.yaml /app/static

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
