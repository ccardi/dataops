from google.cloud import storage
from zipfile import ZipFile
from zipfile import is_zipfile
import io
import os

bucketname = os.environ['BUCKET_NAME']
print(bucketname)
filepath = os.environ['ZIP_PATH']
print(filepath)
cpu_int = os.environ['CPU_INT']
print(cpu_int)

def zipextract(bucketname, zipfilename_with_path):

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucketname)

    destination_blob_pathname = zipfilename_with_path
    
    blob = bucket.blob(destination_blob_pathname)
    zipbytes = io.BytesIO(blob.download_as_string())

    if is_zipfile(zipbytes):
        print("it is a zip file!")
        with ZipFile(zipbytes, 'r') as myzip:
            for contentfilename in myzip.namelist():
                contentfile = myzip.read(contentfilename)
                blob = bucket.blob(zipfilename_with_path + "/" + contentfilename)
                blob.upload_from_string(contentfile)

zipextract(bucketname, filepath) # if the file is gs://mybucket/path/file.zip
x=0
while x<int(cpu_int):
    y=x*x
    x=x+1

print('================ End ==================')
