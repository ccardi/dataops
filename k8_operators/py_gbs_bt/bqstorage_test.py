from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import reader as reA
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
#print(dir(session))
#print(session.ByteSize())

readers=[]
#print(session)
for stream in session.streams:
  readers.append({'session':session,"streamName":stream.name})


reader = client.read_rows(readers[0]['streamName'])


rows = reader.rows(readers[0]['session'])
#print(reader.row_count())
test = reA.ReadRowsIterable(reader, readers[0]['session'])

print((reader.__dict__))

'''
for enum, row in enumerate(rows):
    if enum%10000==0:
       #print(enum)
       pass
'''