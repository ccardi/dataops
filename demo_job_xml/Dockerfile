FROM python:3.9-slim
WORKDIR /srv
COPY ./requirements.txt /srv/requirements.txt
RUN pip3 install -r requirements.txt
COPY xml_to_bq.py /
