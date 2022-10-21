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
num_workers=3
max_num_workers=3
temp_location = 'gs://pod-fr-retail-demo/temp'
staging_location='gs://pod-fr-retail-demo/staging'
column_family_id = "OrderId"
instance_id='test-load'
table_id ='test-load-bq'

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
#options.view_as(SetupOptions).requirements_file='requirements.txt'
#options.view_as(SetupOptions).save_main_session = True
#options.view_as(DebugOptions).experiments = ['shuffle_mode=service,use_runner_v2']
#options.view_as(SetupOptions).requirements_cache='/root/notebook/workspace/20200617'

from google.cloud import bigquery_storage_v1
project_id='pod-fr-retail'
client = bigquery_storage_v1.BigQueryReadClient()
table = "projects/{}/datasets/{}/tables/{}".format(
      "pod-fr-retail", "supply_demo", "virtualshop_orders"
)
requested_session = bigquery_storage_v1.types.ReadSession()
requested_session.table = table
requested_session.data_format = bigquery_storage_v1.enums.DataFormat.AVRO
requested_session.read_options.selected_fields.append("orderId")
#requested_session.read_options.row_restriction = 'state = "WA"'
modifiers = None
parent = "projects/{}".format(project_id)
session = client.create_read_session(
    parent,
    requested_session,
    max_stream_count=30,
)

readers=[]
#print(session)
for stream in session.streams:
  readers.append({'session':session,"streamName":stream.name})

class bqstorage(beam.DoFn):
    def process(self, element):
      from google.cloud import bigquery_storage_v1
      clientbq = bigquery_storage_v1.BigQueryReadClient()
      reader = clientbq.read_rows(element['streamName'])
      rows = reader.rows(element['session'])
      for row in rows:
        yield row


class enrich(beam.DoFn):
    def setup(self):
      from google.cloud.bigtable import row, column_family, Client
      import datetime
      self.row=row
      self.datetime=datetime
    def process(self, element): 
        row_key = element['orderId'].encode()
        direct_row = self.row.DirectRow(row_key=row_key)
        direct_row.set_cell(
            'orderId',
            'orderId',
            str(element['orderId']).encode(),
            timestamp=self.datetime.datetime.utcnow()
        )
        yield direct_row

def run(argv=None):
  with beam.Pipeline(options=options) as p:
    reads=(
        p 
        | "Create " >> beam.Create(readers)
        | "Read orderId" >> beam.ParDo(bqstorage())
        | "transform Into Bigtable direct_row" >>  beam.ParDo(enrich())
        #| "WriteToBT" >> WriteToBigTable(project_id=project,instance_id=instance_id,table_id=table_id)
        )

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
