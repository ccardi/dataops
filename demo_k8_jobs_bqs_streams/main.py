from google.cloud import bigquery_storage_v1
import json
import csv
from google.cloud import storage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--max_streams", help="number_streams", default=3)
parser.add_argument("--bq_projectId", help="projectId", required=True)
parser.add_argument("--bq_dataset", help="dataset", required=True)
parser.add_argument("--bq_tableId", help="tableId", required=True )
parser.add_argument("--spanner_instance", help="spanner_instance", required=True )
parser.add_argument("--spanner_table", help="spanner_table", required=True )
parser.add_argument("--selected_fields", help="selected_fields" )

args = parser.parse_args()
max_streams=int(args.max_streams)
projectId=args.bq_projectId
dataset=args.bq_dataset
tableId=args.bq_tableId
spanner_instance=args.spanner_instance
spanner_table=args.spanner_table
selected_fields=""
if args.selected_fields:
    selected_fields=args.selected_fields.split(",")

def bqstorage_to_spanner(projectId, dataset, tableId, bucket_name, file_prefix, max_rows, selected_fields):
    print("\nStart extract into {}.{} folder \n".format( bucket_name, file_prefix))
    client_bq = bigquery_storage_v1.BigQueryReadClient()
    requested_session = bigquery_storage_v1.types.ReadSession()
    requested_session.data_format = bigquery_storage_v1.types.DataFormat.AVRO
    requested_session.table = "projects/{}/datasets/{}/tables/{}".format( projectId,dataset, tableId)
    requested_session.read_options.selected_fields=selected_fields
    requested_session.read_options.row_restriction="date = CAST('2017-9-27' as DATE)"
    parent = "projects/{}".format(projectId)
    session = client_bq.create_read_session(
        parent=parent,
        read_session=requested_session,
        max_stream_count=max_streams,
    )
    readers=[]
    for stream in session.streams:
        readers.append({"streamName":stream.name})
    #print(readers)
    print(len(readers))
    for reader in readers:
        reader = client_bq.read_rows(reader['streamName'])
        rows = reader.rows()
        i=0  
        for row in rows:
            #row.values()
            i=i+1
        print(i)
    
bqstorage_to_spanner(projectId, dataset, tableId, spanner_instance, spanner_instance, max_streams, selected_fields)


import argparse
import base64
import datetime
import decimal
import json
import logging
import time

from google.cloud import spanner

OPERATION_TIMEOUT_SECONDS = 240
PROJECT_ID="pod-fr-retail"
REGION="europe-west1"

def create_database(instance_id, database_id):
    """Creates a database and tables for sample data."""
    spanner_client = spanner.Client(project=PROJECT_ID)
    config_name = "{}/instanceConfigs/regional-{}".format(
        spanner_client.project_name, PROJECT_ID
    )
    print(spanner_client.project_name)
    instance = spanner_client.instance(instance_id, configuration_name=config_name)

    database = instance.database(
        database_id,
        ddl_statements=[
            """CREATE TABLE Singers (
            SingerId     INT64 NOT NULL,
            FirstName    STRING(1024),
            LastName     STRING(1024),
            SingerInfo   BYTES(MAX),
            FullName   STRING(2048) AS (
                ARRAY_TO_STRING([FirstName, LastName], " ")
            ) STORED
        ) PRIMARY KEY (SingerId)""",
            """CREATE TABLE Albums (
            SingerId     INT64 NOT NULL,
            AlbumId      INT64 NOT NULL,
            AlbumTitle   STRING(MAX)
        ) PRIMARY KEY (SingerId, AlbumId),
        INTERLEAVE IN PARENT Singers ON DELETE CASCADE""",
        ],
    )

    operation = database.create()

    print("Waiting for operation to complete...")
    operation.result(60)

    print("Created database {} on instance {}".format(database_id, instance_id))


#create_database("events-store", "customers-events")

def insert_data(instance_id, database_id):
    """Inserts sample data into the given database.
    The database and table must already exist and can be created using
    `create_database`.
    """
    spanner_client = spanner.Client(project=PROJECT_ID)
    config_name = "{}/instanceConfigs/regional-{}".format(
        spanner_client.project_name, PROJECT_ID
    )
    print(spanner_client.project_name)
    instance = spanner_client.instance(instance_id, configuration_name=config_name)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert_or_update(
            table="Singers",
            columns=("SingerId", "FirstName", "LastName"),
            values=[
                (1, "Marc", "Richards"),
                (2, "Catalina", "Smith"),
                (3, "Alice", "Trentor"),
                (4, "Lea", "Martin"),
                (5, "David", "Lomond"),
            ],
        )
        

        batch.insert_or_update(
            table="Albums",
            columns=("SingerId", "AlbumId", "AlbumTitle"),
            values=[
                (1, 1, "Total Junk"),
                (1, 2, "Go, Go, Go"),
                (2, 1, "Green"),
                (2, 2, "Forever Hold Your Peace"),
                (2, 3, "Terrified"),
            ],
        )

    
    for j in range(1,1000):
        print(j)
        with database.batch() as batch:
                batch.insert_or_update(
                    table="Singers",
                    columns=("SingerId", "FirstName"),
                    values=[
                        (i*j, str(i*j)+"Marcs") for i in range(1,1000)
                    ]
                )
        print("Inserted data.")

insert_data("events-store", "customers-events")