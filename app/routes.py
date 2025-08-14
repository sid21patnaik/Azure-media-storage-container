from flask import Blueprint, render_template, request, redirect, send_file, url_for, session, flash
from werkzeug.utils import secure_filename
from io import BytesIO
import os

# Import your azure_utils functions accordingly
from .azure_utils import list_blobs, download_blob, delete_blob, get_sas_view_url, get_file_stream, container_client

main = Blueprint("main", __name__)

def login_required(f):
    from functools import wraps
    from flask import redirect, url_for

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function

@main.route("/", methods=["GET", "POST"])
@login_required
def upload_file():
    user = session.get("user")

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            filename = secure_filename(file.filename)
            # ✅ Auto-renaming if file exists
            existing_files = [blob.name for blob in container_client.list_blobs()]
            if filename in existing_files:
                name, ext = os.path.splitext(filename)
                counter = 1
                new_filename = f"{name}_{counter}{ext}"
                while new_filename in existing_files:
                    counter += 1
                    new_filename = f"{name}_{counter}{ext}"
                filename = new_filename

            # Save to Azure Blob Storage
            try:
                container_client.upload_blob(
                    name=filename,
                    data=file,
                    overwrite=True
                )
                flash(f"Uploaded file: {filename}", "success")
            except Exception as e:
                flash(f"Upload failed: {e}", "danger")
            return redirect(url_for("main.upload_file"))
        else:
            flash("No file selected", "warning")

    blobs = list_blobs()
    return render_template("index.html", blobs=blobs, user=user)

@main.route("/download/<filename>")
@login_required
def download_file(filename):
    data = download_blob(filename)
    return send_file(BytesIO(data), as_attachment=True, download_name=filename)

@main.route("/view/<filename>")
@login_required
def view_file(filename):
    office_extensions = (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp")

    if filename.lower().endswith(office_extensions):
        sas_url = get_sas_view_url(filename)
        from urllib.parse import quote_plus
        encoded_url = quote_plus(sas_url)
        return redirect(f"https://view.officeapps.live.com/op/embed.aspx?src={encoded_url}")
    else:
        blob_data, mime_type = get_file_stream(filename)
        return send_file(BytesIO(blob_data), mimetype=mime_type)

@main.route("/delete/<filename>")
@login_required
def delete_file(filename):
    try:
        delete_blob(filename)
        flash(f"Deleted file: {filename}", "success")
    except Exception as e:
        flash(f"Delete failed: {e}", "danger")
    return redirect(url_for("main.upload_file"))

@main.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("auth.logout"))

@main.route("/test-session")
def test_session():
    user = session.get("user")
    if user:
        return f"User in session: {user}"
    else:
        return redirect(url_for("auth.login"))
