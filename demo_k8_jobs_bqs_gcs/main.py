from google.cloud import bigquery_storage_v1
import json
import csv
from google.cloud import storage

def bqstorage_to_gcs_csv(project_id, productsDataset, productsTable, bucket_name, file_prefix, max_rows, selected_fields):
    print("\nStart extract into {}.{} folder \n".format( bucket_name, file_prefix))
    client_bq = bigquery_storage_v1.BigQueryReadClient()
    table = "projects/{}/datasets/{}/tables/{}".format( project_id,productsDataset, productsTable)
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