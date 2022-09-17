#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS='/home/cardi/data-pipeline/ker_pipeline/pod-fr-retail-key.json'
cd ker_pipeline/

python main.py \
--runner=DataflowRunner \
--project pod-fr-retail