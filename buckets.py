
SERVICE_ACCOUNT_CREDENTIALS = '/content/gcp_api_connector/resources/service_account_credentials.json'

from google.oauth2 import service_account
from google.cloud import storage
storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_CREDENTIALS)



#CRUD Operations:
# CREATE CREATE CREATE CREATE CREATECREATE CREATE CREATE CREATE CREATE CREATE CREATE CREATE CREATE CREATE
def create_bucket(bucket_name):
    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name)
        print('Bucket {} created'.format(bucket.name))
    else:
        print('Bucket {} already exists'.format(bucket.name))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


# READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ READ
def list_buckets():
  buckets = list(storage_client.list_buckets())
  return buckets

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print(blob.name)

def download_bucket(bucket_name, destination_directory):
    #Creates a directory to store the files
    import os
    #Checks if the directory exists
    if not os.path.exists(destination_directory):
        #Creates the directory 
        os.mkdir(destination_directory)
    #Downloads all the files in the bucket
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        blob.download_to_filename(destination_directory + '/' + blob.name)
        print('Blob {} downloaded to {}.'.format(
        blob.name,
        destination_directory + '/' + blob.name))



def download_blob(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(source_blob_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        source_blob_name))


# UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE UPDATE






# DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE DELETE  

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print('Blob {} deleted.'.format(blob_name))

def empty_bucket(bucket_name):
    """Deletes all blobs in the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()

    print('All blobs in {} have been deleted.'.format(bucket.name))

def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    bucket = storage_client.bucket(bucket_name)
    bucket.delete()

    print('Bucket {} deleted'.format(bucket.name))



