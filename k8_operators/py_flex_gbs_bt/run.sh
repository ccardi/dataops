#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS='/home/cardi/data-pipeline/ker_pipeline/pod-fr-retail-key.json'
cd ker_pipeline/

python main.py \
--runner=DataflowRunner \
--project pod-fr-retail

PROJECT=pod-fr-retail
export TEMPLATE_IMAGE="gcr.io/$PROJECT/samples/dataflow/bqs-to-bt-beam:latest"
gcloud builds submit --tag "$TEMPLATE_IMAGE" .

BUCKET=pod-fr-retail-demo
export TEMPLATE_PATH="gs://$BUCKET/samples/dataflow/templates/bqs-to-bt-beam.json"
# Build the Flex Template.
gcloud beta dataflow flex-template build $TEMPLATE_PATH \
  --image "$TEMPLATE_IMAGE" \
  --sdk-language "PYTHON" \
  --metadata-file "metadata.json"

gcloud beta dataflow flex-template run "bqs-to-bt-beam-`date +%Y%m%d-%H%M%S`" \
  --template-file-gcs-location "$TEMPLATE_PATH" \
  --region=europe-west1 \
  --parameters experiments="disable_flex_template_entrypoint_overrride"