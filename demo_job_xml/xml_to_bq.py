import os
import pandas
import pandas_gbq

print('================ Start ==================')

project_id = os.environ['PROJECT_ID']
gcs_xml_path= os.environ['GCS_XML_PATH']
xpath= os.environ['XML_XPATH']
namespaces= {"doc":os.environ['XML_XPATH']}

destination_table = os.environ['TABLE_ID']
location='EU'

df = pd.read_xml(
    gcs_xml_path
    , xpath='.//doc:price-table'
    , namespaces=namespaces
)

df.to_gbq(destination_table=destination_table, project_id=project_id,location=location, if_exists="replace")

print('================ End ==================')
