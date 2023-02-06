FROM python:3.7
ADD pubsubOrders.py /
ADD refproduct.json /
ADD repartition_age.json /
ADD repartition_gender.json /
ADD repartition_takeaway.json /
ADD repartition_paiement.json /
ADD repartition_panier.json /
ADD trendsByCity.json /
RUN pip install --upgrade google-cloud-pubsub
CMD [ "python", "./pubsubOrders.py" ]