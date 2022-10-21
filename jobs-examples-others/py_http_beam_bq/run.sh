#!/bin/bash
python3 main.py \
--runner=DataflowRunner \
--project pod-fr-retail \
--input gs://pod-fr-retail-kering/report_ids/ids-*.csv \
--output gs://pod-fr-retail-kering/test \
--staging_location gs://pod-fr-retail-kering/staging \
--temp_location gs://pod-fr-retail-kering/temp \
--zone europe-west1-c \
--region europe-west1 \
--worker_machine_type n1-standard-1 \
--num_workers 2 \
--max_num_workers 3 \
--url 'http://test.com'