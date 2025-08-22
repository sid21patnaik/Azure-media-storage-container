from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import os, mimetypes

# --------------------------
# Azure Storage Config
# --------------------------
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# --------------------------
# List blobs
# --------------------------
def list_blobs():
    """Return list of all blobs in container"""
    return container_client.list_blobs()

# --------------------------
# Download blob
# --------------------------
def download_blob(filename):
    """Download blob data as bytes"""
    blob_client = container_client.get_blob_client(filename)
    return blob_client.download_blob().readall()

# --------------------------
# Delete blob
# --------------------------
def delete_blob(filename):
    """Delete a blob from container"""
    blob_client = container_client.get_blob_client(filename)
    blob_client.delete_blob()

# --------------------------
# Generate SAS URL for viewing
# --------------------------
def get_sas_view_url(filename):
    """
    Generate temporary SAS URL (1 hour) for viewing Office files in browser
    """
    blob_client = container_client.get_blob_client(filename)
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=CONTAINER_NAME,
        blob_name=filename,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    return f"{blob_client.url}?{sas_token}"

# --------------------------
# Stream blob with MIME type
# --------------------------
def get_file_stream(filename):
    """
    Return blob data and MIME type for streaming in browser
    """
    blob_client = container_client.get_blob_client(filename)
    blob_data = blob_client.download_blob().readall()
    mime_type, _ = mimetypes.guess_type(filename)
    return blob_data, mime_type or "application/octet-stream"
