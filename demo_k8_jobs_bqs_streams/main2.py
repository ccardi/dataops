from google.cloud import bigquery_storage_v1
from google.cloud import bigquery
import json
import csv
from google.cloud import storage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--bq_projectId", help="projectId", required=True)
parser.add_argument("--bq_dataset", help="dataset", required=True)
parser.add_argument("--bq_tableId", help="tableId", required=True)

args = parser.parse_args()

projectId=args.bq_projectId
dataset=args.bq_dataset
tableId=args.bq_tableId


def bq_schema(projectId, dataset,tableId):
    # Construct a BigQuery client object.
    client = bigquery.Client()
    table = client.get_table("{}.{}.{}".format(projectId,dataset,tableId))  # Make an API request.

        # View table properties
    print(
        "Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id)
    )
    print("Table schema: {}".format(table.schema))
    print("Table description: {}".format(table.description))
    print("Table has {} rows".format(table.num_rows))
    for field in table.schema:
        print(field)        

bq_schema(projectId, dataset,tableId)