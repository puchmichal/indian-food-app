FROM python:3.7-slim-buster

RUN pip install -U pip setuptools
RUN apt-get update
RUN apt-get install build-essential -y

COPY . .
RUN pip install --root / install -r requirements.txt

CMD exec gunicorn --workers 4 --timeout=900 --threads 4 run:app