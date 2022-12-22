FROM python:3.10-slim-bullseye
WORKDIR /srv
COPY ./requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt
COPY main.py /
