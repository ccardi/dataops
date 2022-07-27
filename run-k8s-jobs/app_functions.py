from google.cloud import container_v1
import google.auth
import google.auth.transport.requests
import kubernetes
from kubernetes.client import V1Job
from kubernetes import client as kubernetes_client
from tempfile import NamedTemporaryFile
import base64
from time import sleep
import logging
import yaml
from google.cloud import storage

def get_k8s_client(project_id: str, location: str,
                   cluster_id: str) -> kubernetes.client.CoreV1Api:
    container_client = google.cloud.container_v1.ClusterManagerClient()
    request = {
        "name": f"projects/{project_id}/locations/{location}/clusters/{cluster_id}"
    }
    response = container_client.get_cluster(request=request)
    creds, projects = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    configuration = kubernetes.client.Configuration()
    configuration.host = f'https://{response.endpoint}'
    with NamedTemporaryFile(delete=False) as ca_cert:
        ca_cert.write(base64.b64decode(response.master_auth.cluster_ca_certificate))
        configuration.ssl_ca_cert = ca_cert.name
    configuration.api_key_prefix['authorization'] = 'Bearer'
    configuration.api_key['authorization'] = creds.token

    return kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(configuration))

def create_job_from_gcs(bucket_name, source_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    json_data = blob.download_as_string()
    job= yaml.safe_load(json_data)
    return job

def create_job_from_file(yaml_path):
    with open(yaml_path) as file:
        job = yaml.safe_load(file)
    return job

def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace="default")
    logging.info("Job created.")
    #get_job_status(api_instance,job)

def get_job_status(api_instance,job):
    job_completed = False
    while not job_completed:
        api_response = api_instance.read_namespaced_job_status(
            name=job['metadata']['name'],
            namespace="default")
        if api_response.status.succeeded is not None or \
                api_response.status.failed is not None:
            job_completed = True
        sleep(10)
        logging.info("Job status='%s'" % str(api_response.status))



