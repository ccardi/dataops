from google.cloud import bigquery_storage_v1
import json
import csv
from google.cloud import storage
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--max_rows", help="number_rows", default=20000)
parser.add_argument("--projectId", help="projectId", required=True)
parser.add_argument("--dataset", help="dataset", required=True)
parser.add_argument("--tableId", help="tableId", required=True )
parser.add_argument("--selected_fields", help="selected_fields" )
parser.add_argument("--bucket_name", help="bucket_name", required=True )
parser.add_argument("--file_prefix", help="file_prefix", required=True )

args = parser.parse_args()
max_rows=int(args.max_rows)
projectId=args.projectId
dataset=args.dataset
tableId=args.tableId
bucket_name=args.bucket_name
file_prefix=args.file_prefix
selected_fields=""
if args.selected_fields:
    selected_fields=args.selected_fields.split(",")

def bqstorage_to_gcs_csv(projectId, dataset, tableId, bucket_name, file_prefix, max_rows, selected_fields):
    print("\nStart extract into {}.{} folder \n".format( bucket_name, file_prefix))
    client_bq = bigquery_storage_v1.BigQueryReadClient()
    requested_session = bigquery_storage_v1.types.ReadSession()
    requested_session.data_format = bigquery_storage_v1.types.DataFormat.AVRO
    requested_session.table = "projects/{}/datasets/{}/tables/{}".format( projectId,dataset, tableId)
    requested_session.read_options.selected_fields=selected_fields
    parent = "projects/{}".format(projectId)
    session = client_bq.create_read_session(
        parent=parent,
        read_session=requested_session,
        max_stream_count=1,
    )
    readers=[]
    for stream in session.streams:
        readers.append({"streamName":stream.name})
    reader = client_bq.read_rows(readers[0]['streamName'])
    rows = reader.rows()
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    row_number=0
    file_suffix_number=round(row_number/max_rows)  
    for row in rows:
        if row_number%max_rows==0:
            if row_number>=max_rows:
                f.close()
            file_suffix_number=round(row_number/max_rows)
            blob = bucket.blob(file_prefix+str(file_suffix_number))
            f=blob.open("w")
            w = csv.writer(f)
            print(bucket_name+"/" +file_prefix+str(file_suffix_number)+" created")
        row_number=row_number+1
        w.writerow(row.values())
    print("\nExtract {} rows into {}.{}[0-{}]  ".format(row_number, bucket_name, file_prefix, file_suffix_number))

bqstorage_to_gcs_csv(projectId, dataset, tableId, bucket_name, file_prefix, max_rows, selected_fields)