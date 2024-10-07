import google.auth
from google.cloud import storage
import pandas as pd
import os
#requirements.txt
# google-cloud-storage==1.30.0
# gcsfs==0.6.2   pip3 install gcsfs
# pandas==1.1.0  pip3 install pandas
# fsspec              pip3 install fsspec

#custom function to read data in json file
def get_csv_gcs(bucket_name, file_name, api_key_path):
    # Set the environment variable for the Google API key
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key_path
    
    # Authenticate and create a client
    credentials, project = google.auth.default()
    client = storage.Client(credentials=credentials, project=project)
    
    # Get the bucket and blob
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    # Download the blob as a string
    csv_data = blob.download_as_string()
    
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(pd.compat.StringIO(csv_data.decode('utf-8')))
    return df

bucket_name = "collyers-main-bucket"
file_name = "acs-f2-datasetOG.csv"
api_key_path = 'gcloud-test/collyers-435813-5d45d9974b4f.json'
csv_data = get_csv_gcs(bucket_name, file_name, api_key_path)
print(csv_data.head(5))