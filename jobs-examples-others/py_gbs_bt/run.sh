#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS='/home/cardi/data-pipeline/ker_pipeline/pod-fr-retail-key.json'
cd ker_pipeline/

python main.py \
--runner=DataflowRunner \
--project pod-fr-retail


python -m main \
    --runner DataflowRunner \
    --project pod-fr-retail \
    --template_location gs://pod-fr-retail-demo/templates/gbs_to_bt

gcloud dataflow jobs run gbs_to_bq2 \
    --gcs-location gs://pod-fr-retail-demo/templates/gbs_to_bt \
    --region europe-west1

curl -H \
"Authorization: Bearer $(gcloud auth print-identity-token)" \
https://bigquery-sq.clients6.google.com/v3/projects/486742359899/savedQueries?key=AIzaSyCI-zsRP85UVOi0DjtiCwWBwQ1djDy741g