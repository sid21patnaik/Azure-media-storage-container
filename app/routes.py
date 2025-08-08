from app.decorators import login_required
from flask import Blueprint, render_template, request, redirect, send_file, url_for, session
from .azure_utils import (
    list_blobs, upload_blob, download_blob, delete_blob,
    get_sas_view_url, get_file_stream
)
from io import BytesIO
from datetime import datetime
from urllib.parse import quote_plus
from werkzeug.utils import secure_filename
from app.azure_utils import container_client
import os
from flask import flash

main = Blueprint('main', __name__)

@main.route("/ping")
def ping():
    return "App is running!"

@main.route("/", methods=["GET", "POST"])
@login_required
def upload_file():
    from app.auth import get_token_from_cache
    token = get_token_from_cache()
    if not token:
        return redirect(url_for("auth.login"))

    session["user"] = token.get("id_token_claims", {})  # Add default fallback
    print("👤 User in session:", session.get("user"))  # Debug log

    if request.method == "POST":
        file = request.files.get('file')
        if file:
            original_filename = secure_filename(file.filename)
            name, ext = os.path.splitext(original_filename)
            new_filename = original_filename

            existing_blobs = [blob.name for blob in container_client.list_blobs()]
            if new_filename in existing_blobs:
                i = 1
                while True:
                    candidate_name = f"{name}({i}){ext}"
                    if candidate_name not in existing_blobs:
                        new_filename = candidate_name
                        flash(f"File already exists. Renamed to: {new_filename}", "warning")
                        break
                    i += 1
            else:
                flash(f"Uploaded file: {new_filename}", "success")

            blob_client = container_client.get_blob_client(new_filename)
            blob_client.upload_blob(file, overwrite=False)
            return redirect(url_for("main.upload_file"))

    blobs = list_blobs()
    return render_template("index.html", blobs=blobs, user=session.get("user"))

@main.route("/download/<filename>")
@login_required
def download_file(filename):
    from app.auth import get_token_from_cache
    token = get_token_from_cache()
    if not token:
        return redirect(url_for("auth.login"))
    session["user"] = token.get("id_token_claims", {})

    data = download_blob(filename)
    return send_file(BytesIO(data), as_attachment=True, download_name=filename)

@main.route("/view/<filename>")
@login_required
def view_file(filename):
    from app.auth import get_token_from_cache
    token = get_token_from_cache()
    if not token:
        return redirect(url_for("auth.login"))
    session["user"] = token.get("id_token_claims", {})

    office_extensions = (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp")

    if filename.lower().endswith(office_extensions):
        sas_url = get_sas_view_url(filename)
        encoded_url = quote_plus(sas_url)
        return redirect(f"https://view.officeapps.live.com/op/embed.aspx?src={encoded_url}")
    else:
        blob_data, mime_type = get_file_stream(filename)
        return send_file(BytesIO(blob_data), mimetype=mime_type)

@main.route("/delete/<filename>")
@login_required
def delete_file(filename):
    from app.auth import get_token_from_cache
    token = get_token_from_cache()
    if not token:
        return redirect(url_for("auth.login"))
    session["user"] = token.get("id_token_claims", {})

    try:
        delete_blob(filename)
        return redirect(url_for("main.upload_file"))
    except Exception as e:
        return f"Delete failed: {e}", 500

@main.route("/session-debug")
def session_debug():
    return {"user": session.get("user"), "token_cache": session.get("token_cache")}
