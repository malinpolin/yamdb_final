FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

COPY ./static/ /app/api_yamdb

CMD ["/bin/bash", "./entrypoint.sh"]
