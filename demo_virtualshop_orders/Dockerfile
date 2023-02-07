FROM python:3.8-slim-buster
WORKDIR /srv
COPY ./requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt
COPY pubsubOrders.py /
COPY refproduct.json /
COPY repartition_age.json /
COPY repartition_gender.json /
COPY repartition_takeaway.json /
COPY repartition_paiement.json /
COPY repartition_panier.json /
COPY trendsByCity.json /
CMD [ "python3", "/pubsubOrders.py" ]