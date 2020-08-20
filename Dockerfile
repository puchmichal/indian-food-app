FROM python:3.7-slim-buster

RUN pip install -U pip setuptools
RUN apt-get update
RUN apt-get install build-essential -y

COPY . .
RUN pip install --root / install -r requirements.txt

CMD flask db init
CMD flask db merge -m "docker build merge"
CMD flask db upgrade

EXPOSE 5000

CMD exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout=900 --threads 4 run:app