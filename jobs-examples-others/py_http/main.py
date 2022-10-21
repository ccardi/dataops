import requests
import time
import json
import argparse
from google.cloud import storage

#file_name='reports_ids.json'
#bucket='pod-fr-retail'
#file_path='airflow/input/'+file_name

parser = argparse.ArgumentParser()
parser.add_argument('--outputFileName',
                    required=True,
                    help='Output fileName')
parser.add_argument('--outputBucket',
                    required=True,
                    help='Output bucket')
parser.add_argument('--outputPath',
                    required=True,
                    help='outputPath file to write results to.')
args = parser.parse_args()

print(args.outputFileName)

# Instantiates a client
storage_client = storage.Client()
f = open(args.outputFileName, "a")

ids=range(1,3)
for j in range(1,4):
  for i in ids:
    f.write(json.dumps({'page':j , 'id': str(i)+'-'+str(j), 'otherData':'' })+'\n')

f.close()
bucket = storage_client.bucket(args.outputBucket)
blob = bucket.blob(args.outputPath + args.outputFileName)
blob.upload_from_filename(args.outputFileName)