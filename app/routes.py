from flask import Blueprint, render_template, request, redirect, send_file, url_for
from .azure_utils import (
    list_blobs, upload_blob, download_blob, delete_blob,
    get_sas_view_url, get_file_stream
)
from io import BytesIO
from datetime import datetime
from urllib.parse import quote_plus
from werkzeug.utils import secure_filename
from app.azure_utils import container_client
import mimetypes
import os

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files['file']
        if file:
            original_filename = secure_filename(file.filename)
            name, ext = os.path.splitext(original_filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{name}_{timestamp}{ext}"

            blob_client = container_client.get_blob_client(new_filename)
            blob_client.upload_blob(file, overwrite=False)
            return redirect(url_for("main.upload_file"))
        
    blobs = list_blobs()
    return render_template("index.html", blobs=blobs)


@main.route("/download/<filename>")
def download_file(filename):
    data = download_blob(filename)
    return send_file(BytesIO(data), as_attachment=True, download_name=filename)


@main.route("/view/<filename>")
def view_file(filename):
    office_extensions = (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp")

    if filename.lower().endswith(office_extensions):
        sas_url = get_sas_view_url(filename)
        encoded_url = quote_plus(sas_url)
        return redirect(f"https://view.officeapps.live.com/op/embed.aspx?src={encoded_url}")
    else:
        blob_data, mime_type = get_file_stream(filename)
        return send_file(BytesIO(blob_data), mimetype=mime_type)


@main.route("/delete/<filename>")
def delete_file(filename):
    try:
        delete_blob(filename)
        return redirect(url_for("main.upload_file"))
    except Exception as e:
        return f"Delete failed: {e}", 500