from google.cloud import bigquery_storage_v1
import json
import csv
from google.cloud import storage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--max_rows", help="number_rows", default=20000)
parser.add_argument("--project_id", help="project_id", required=True)
parser.add_argument("--dataset", help="dataset", required=True)
parser.add_argument("--tableId", help="tableId", required=True )
parser.add_argument("--productsetId", help="productsetId", required=True )
parser.add_argument("--bucket_name", help="bucket_name", required=True )
parser.add_argument("--file_prefix", help="file_prefix", required=True )
parser.add_argument("--selected_fields", help="selected_fields", required=True )

args = parser.parse_args()

max_rows=int(args.max_rows)
project_id=args.project_id
dataset=args.dataset
tableId=args.tableId
selected_fields=args.selected_fields.split(",")
productsetId=args.productsetId
bucket_name=args.bucket_name
file_prefix=args.file_prefix


def bqstorage_to_gcs_csv(project_id, dataset, tableId, bucket_name, file_prefix, max_rows, selected_fields):
    print("\nStart extract into {}.{} folder \n".format( bucket_name, file_prefix))
    client_bq = bigquery_storage_v1.BigQueryReadClient()
    table = "projects/{}/datasets/{}/tables/{}".format( project_id,dataset, tableId)
    requested_session = bigquery_storage_v1.types.ReadSession()
    requested_session.table = table
    requested_session.data_format = bigquery_storage_v1.types.DataFormat.AVRO
    selected_fields=selected_fields
    requested_session.read_options.selected_fields=selected_fields
    modifiers = None
    parent = "projects/{}".format(project_id)
    session = client_bq.create_read_session(
        parent=parent,
        read_session=requested_session,
        max_stream_count=1,
    )

    readers=[]
    for stream in session.streams:
        readers.append({'session':session,"streamName":stream.name})
    reader = client_bq.read_rows(readers[0]['streamName'])
    rows = reader.rows(readers[0]['session'])
    i=0
    file_suffix_number=round(i/max_rows)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_prefix+str(file_suffix_number))
    f=blob.open("w")
    for row in rows:
        if i%max_rows==0:
            if f:
                f.close()
            file_suffix_number=round(i/max_rows)
            blob = bucket.blob(file_prefix+str(file_suffix_number))
            f = blob.open("w")
            w = csv.writer(f)
            print(bucket_name+"/" +file_prefix+str(file_suffix_number)+" created")
        i=i+1
        w.writerow(row.values())
    print("\nExtract {} rows into {}.{}[0-{}]  ".format(i, bucket_name, file_prefix, file_suffix_number))



bqstorage_to_gcs_csv(project_id, dataset, tableId, bucket_name, file_prefix, max_rows, selected_fields)