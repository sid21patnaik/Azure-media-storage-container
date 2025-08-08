from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os, mimetypes
import urllib.parse

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def list_blobs():
    return container_client.list_blobs()

def upload_blob(file):
    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file, overwrite=True)

def download_blob(filename):
    blob_client = container_client.get_blob_client(filename)
    return blob_client.download_blob().readall()

def delete_blob(filename):
    blob_client = container_client.get_blob_client(filename)
    blob_client.delete_blob()

def get_sas_view_url(filename):
    blob_client = container_client.get_blob_client(filename)
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=filename,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    # Construct final SAS URL (no double encoding)
    sas_url = f"{blob_client.url}?{sas_token}"
    return sas_url  # return raw SAS URL


def get_file_stream(filename):
    blob_client = container_client.get_blob_client(filename)
    blob_data = blob_client.download_blob().readall()
    mime_type, _ = mimetypes.guess_type(filename)
    return blob_data, mime_type or "application/octet-stream"