import requests
import time
import json
from google.cloud import storage

# Instantiates a client
storage_client = storage.Client()
f = open("reports_ids.json", "a")

ids=range(1,3)
for j in range(1,4):
  for i in ids:
    f.write(json.dumps({'page':j , 'id': str(i)+'-'+str(j), 'otherData':'' })+'\n')
f.close()
bucket = storage_client.bucket('pod-fr-retail')
blob = bucket.blob('airflow/input/reports_ids.json')
blob.upload_from_filename('reports_ids.json')