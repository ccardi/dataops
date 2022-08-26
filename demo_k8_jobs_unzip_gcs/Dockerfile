FROM python:3.8-slim-buster
WORKDIR /srv
COPY ./requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt
COPY gcs_unzip.py /
