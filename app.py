import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from dotenv import load_dotenv
from io import BytesIO
import mimetypes
from urllib.parse import quote_plus
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def get_storage_account_name(conn_str):
    for part in conn_str.split(';'):
        if part.startswith('AccountName='):
            return part.split('=')[1]
    return None

STORAGE_ACCOUNT_NAME = get_storage_account_name(AZURE_STORAGE_CONNECTION_STRING)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            blob_client = container_client.get_blob_client(file.filename)
            blob_client.upload_blob(file, overwrite=True)
            return redirect(url_for("upload_file"))

    blobs = [{"name": blob.name} for blob in container_client.list_blobs()]
    return render_template("index.html", blobs=blobs)

@app.route("/download/<filename>")
def download_file(filename):
    try:
        blob_client = container_client.get_blob_client(filename)
        blob_data = blob_client.download_blob().readall()
        return send_file(BytesIO(blob_data), as_attachment=True, download_name=filename)
    except Exception as e:
        return f"Download failed: {e}", 500

@app.route("/view/<filename>")
def view_file(filename):
    try:
        mime_type, _ = mimetypes.guess_type(filename)
        mime_type = mime_type or 'application/octet-stream'

        if filename.lower().endswith('.docx'):
            blob_client = container_client.get_blob_client(filename)
            blob_url = blob_client.url  # Use SDK URL

            sas_token = generate_blob_sas(
                account_name=STORAGE_ACCOUNT_NAME,
                container_name=CONTAINER_NAME,
                blob_name=filename,
                account_key=blob_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=1)
            )
            blob_url_with_sas = f"{blob_url}?{sas_token}"

            # Debug print to console/log
            print(f"SAS URL for viewing .docx: {blob_url_with_sas}")

            office_viewer_url = f"https://view.officeapps.live.com/op/view.aspx?src={quote_plus(blob_url_with_sas)}"
            return redirect(office_viewer_url)

        blob_client = container_client.get_blob_client(filename)
        stream = blob_client.download_blob()
        file_data = BytesIO(stream.readall())

        allowed_mime_types = ['application/pdf', 'image/png', 'image/jpeg', 'text/plain']
        if mime_type not in allowed_mime_types:
            return "Viewing not supported for this file type.", 415

        return send_file(file_data, mimetype=mime_type)
    except Exception as e:
        return f"View failed: {e}", 500

@app.route("/delete/<filename>", methods=["GET", "POST"])
def delete_file(filename):
    try:
        blob_client = container_client.get_blob_client(filename)
        blob_client.delete_blob()
        return redirect(url_for("upload_file"))
    except Exception as e:
        return f"Delete failed: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)
