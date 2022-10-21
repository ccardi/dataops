import apache_beam as beam
from apache_beam.io.gcp.bigquery import ReadFromBigQuery
from apache_beam.io.gcp.bigtableio import WriteToBigTable
from apache_beam.runners import DataflowRunner
from apache_beam.options import pipeline_options
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import WorkerOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import DebugOptions
from datetime import timedelta
import datetime
import google.auth
import argparse
import logging

project='pod-fr-retail'

zone='europe-west1-c'
region='europe-west1'
worker_machine_type='n1-standard-1' #g1-small
num_workers=30
max_num_workers=30
temp_location = 'gs://pod-fr-retail-demo/temp'
staging_location='gs://pod-fr-retail-demo/staging'
column_family_id = "OrderId"

instance_id='test-load'
table_id ='test-load-bq'

query='SELECT orderId FROM supply_demo.virtualshop_orders'

# Setting up the Beam pipeline options.
options = pipeline_options.PipelineOptions()
#options.view_as(pipeline_options.StandardOptions).streaming = False

_,options.view_as(GoogleCloudOptions).project = google.auth.default()
options.view_as(GoogleCloudOptions).region = region
options.view_as(GoogleCloudOptions).staging_location = staging_location
options.view_as(GoogleCloudOptions).temp_location = temp_location

options.view_as(WorkerOptions).worker_zone = zone
options.view_as(WorkerOptions).machine_type = worker_machine_type
options.view_as(WorkerOptions).num_workers = num_workers
#options.view_as(WorkerOptions).max_num_workers = max_num_workers
options.view_as(WorkerOptions).autoscaling_algorithm='NONE'

options.view_as(SetupOptions).requirements_file='requirements.txt'
#options.view_as(DebugOptions).experiments = ['shuffle_mode=service,use_runner_v2']
#options.view_as(SetupOptions).requirements_cache='/root/notebook/workspace/20200617'

class enrich(beam.DoFn):
    def process(self, element):
        from google.cloud.bigtable import row, column_family, Client
        import datetime
        row_key = element['orderId'].encode()
        direct_row = row.DirectRow(row_key=row_key)
        direct_row.set_cell(
            'orderId',
            'orderId',
            str(element['orderId']).encode(),
            timestamp=datetime.datetime.utcnow()
        )
        yield direct_row

def run(argv=None):
  with beam.Pipeline(options=options) as p:
    reads=(
        p 
        | "Read orderId" >> beam.io.ReadFromAvro('gs://pod-fr-retail-demo/avro/orders*.avro') #beam.io.Read(beam.io.BigQuerySource(query=query,use_standard_sql=True))
        | "transform Into Bigtable direct_row" >>  beam.ParDo(enrich())
        | "WriteToBT" >> WriteToBigTable(project_id=project,instance_id=instance_id,table_id=table_id)
        )

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()