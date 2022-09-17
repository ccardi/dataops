# Use the official lightweight Node.js 12 image.
# https://hub.docker.com/_/node
FROM python:3.7-slim-buster
COPY requirements.txt /
RUN pip install -r requirements.txt
ADD main.py /
