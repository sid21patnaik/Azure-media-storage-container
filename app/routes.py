from flask import Blueprint, render_template, request, redirect, send_file, url_for, session, flash
from werkzeug.utils import secure_filename
from io import BytesIO
import os

# Import helper functions from azure_utils
from .azure_utils import (
    list_blobs,
    download_blob,
    delete_blob,
    get_sas_view_url,
    get_file_stream,
    container_client
)

# Define a Blueprint for the main routes
main = Blueprint("main", __name__)


# --------------------------
# Authentication Middleware
# --------------------------
def login_required(f):
    """
    Decorator to protect routes from unauthorized access.
    Redirects to login page if user is not in session.
    """
    from functools import wraps
    from flask import redirect, url_for

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):  # Check if user exists in session
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


# --------------------------
# File Upload & List Route
# --------------------------
@main.route("/", methods=["GET", "POST"])
@login_required
def upload_file():
    """
    - GET: List all uploaded blobs.
    - POST: Upload a new file to Azure Blob Storage.
    Includes auto-renaming if filename already exists.
    """
    user = session.get("user")

    if request.method == "POST":
        file = request.files.get("file")  # Retrieve uploaded file

        if file:
            filename = secure_filename(file.filename)  # Sanitize filename

            # Check existing blobs in the container
            existing_files = [blob.name for blob in container_client.list_blobs()]

            # If file already exists, auto-rename by appending counter
            if filename in existing_files:
                name, ext = os.path.splitext(filename)
                counter = 1
                new_filename = f"{name}_{counter}{ext}"
                while new_filename in existing_files:
                    counter += 1
                    new_filename = f"{name}_{counter}{ext}"
                filename = new_filename

            # Upload file to Azure Blob Storage
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

    # List blobs to display on UI
    blobs = list_blobs()
    return render_template("index.html", blobs=blobs, user=user)


# --------------------------
# File Download Route
# --------------------------
@main.route("/download/<filename>")
@login_required
def download_file(filename):
    """
    Download a blob from Azure Storage as an attachment.
    """
    data = download_blob(filename)
    return send_file(BytesIO(data), as_attachment=True, download_name=filename)


# --------------------------
# File View Route
# --------------------------
@main.route("/view/<filename>")
@login_required
def view_file(filename):
    """
    - If file is an Office document → open via Office Online Viewer.
    - Else → stream directly in browser with correct MIME type.
    """
    office_extensions = (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp")

    if filename.lower().endswith(office_extensions):
        # Generate SAS URL for Office Online Viewer
        sas_url = get_sas_view_url(filename)
        from urllib.parse import quote_plus
        encoded_url = quote_plus(sas_url)
        return redirect(f"https://view.officeapps.live.com/op/embed.aspx?src={encoded_url}")
    else:
        # Stream non-office file directly in browser
        blob_data, mime_type = get_file_stream(filename)
        return send_file(BytesIO(blob_data), mimetype=mime_type)


# --------------------------
# File Delete Route
# --------------------------
@main.route("/delete/<filename>")
@login_required
def delete_file(filename):
    """
    Delete a file from Azure Blob Storage.
    """
    try:
        delete_blob(filename)
        flash(f"Deleted file: {filename}", "success")
    except Exception as e:
        flash(f"Delete failed: {e}", "danger")

    return redirect(url_for("main.upload_file"))


# --------------------------
# Logout Route
# --------------------------
@main.route("/logout")
@login_required
def logout():
    """
    Clear session and redirect to auth.logout.
    """
    session.clear()
    return redirect(url_for("auth.logout"))


# --------------------------
# Test Session Route
# --------------------------
@main.route("/test-session")
def test_session():
    """
    Debug route to confirm if user is stored in session.
    """
    user = session.get("user")
    if user:
        return f"User in session: {user}"
    else:
        return redirect(url_for("auth.login"))
