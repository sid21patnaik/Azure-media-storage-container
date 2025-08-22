from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os, mimetypes

# --------------------------
# Azure Storage Configuration
# --------------------------
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

# Create Blob service and container clients
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)


# --------------------------
# List all blobs
# --------------------------
def list_blobs():
    """
    Returns a generator of blobs inside the container.
    """
    return container_client.list_blobs()


# --------------------------
# Upload blob
# --------------------------
def upload_blob(file):
    """
    Uploads a file to Azure Blob Storage.
    """
    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file, overwrite=True)


# --------------------------
# Download blob (raw bytes)
# --------------------------
def download_blob(filename):
    """
    Downloads blob content as raw bytes.
    """
    blob_client = container_client.get_blob_client(filename)
    return blob_client.download_blob().readall()


# --------------------------
# Delete blob
# --------------------------
def delete_blob(filename):
    """
    Deletes a blob from storage.
    """
    blob_client = container_client.get_blob_client(filename)
    blob_client.delete_blob()


# --------------------------
# Get SAS URL for viewing
# --------------------------
def get_sas_view_url(filename):
    """
    Generates a temporary SAS URL for viewing a blob.
    """
    blob_client = container_client.get_blob_client(filename)
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=container_name,
        blob_name=filename,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)  # URL valid for 1 hour
    )
    return f"{blob_client.url}?{sas_token}"


# --------------------------
# Get file as stream + MIME
# --------------------------
def get_file_stream(filename):
    """
    Returns blob as (file_stream, mime_type).
    """
    blob_client = container_client.get_blob_client(filename)
    blob_data = blob_client.download_blob().readall()

    # Guess MIME type or default to binary
    mime_type, _ = mimetypes.guess_type(filename)
    return blob_data, mime_type or "application/octet-stream"
