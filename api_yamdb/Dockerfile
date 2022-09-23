FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD ["/bin/bash", "./entrypoint.sh"]

COPY /static/redoc.yaml /app/static
