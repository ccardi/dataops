import os
import base64
import json
from flask import Flask, render_template,  request
import logging
import random
import string
import google.cloud.logging
from app_functions import get_k8s_client,create_job,create_job_from_gcs

# pylint: disable=C0103
app = Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    data = request.get_json()
    client = google.cloud.logging.Client()
    client.setup_logging()
    logging.info("=====message======")
    logging.info(data)
    logging.info("=====message (end)======")
    kub=get_k8s_client(data["projectId"],data["region"],data["gkeClusterName"])
    job=create_job_from_gcs(data["jobStorageBucket"],data["jobPathName"])
    letters=string.ascii_lowercase
    job['metadata']['name']=data["jobRootName"] + ''.join(random.choice(letters) for i in range(4))
    create_job(kub,job)

    return "Job created: " + job['metadata']['name'] + "\n"


@app.route("/pubsub", methods=["POST"])
def index():
    client = google.cloud.logging.Client()
    client.setup_logging()
    
    envelope = request.get_json()
    
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        data_string = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()
        data=json.loads(data_string)
        logging.info("=====message======")
        logging.info(data_string)
        logging.info("=====message (end)======")
        kub=get_k8s_client(data["projectId"],data["region"],data["gkeClusterName"])
        job=create_job_from_gcs(data["jobStorageBucket"],data["jobPathName"])
        letters=string.ascii_lowercase
        job['metadata']['name']=data["jobRootName"] + ''.join(random.choice(letters) for i in range(4))
        create_job(kub,job)

    return (f"", 204)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
