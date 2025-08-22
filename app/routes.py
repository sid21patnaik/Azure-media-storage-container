from flask import Blueprint, render_template, request, redirect, send_file, url_for, session, flash
from werkzeug.utils import secure_filename
from io import BytesIO
import os

# Import Azure helper functions
from .azure_utils import list_blobs, download_blob, delete_blob, get_sas_view_url, get_file_stream, container_client

main = Blueprint("main", __name__)

# --------------------------
# Login required decorator
# --------------------------
def login_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:  # If user not logged in → redirect
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


# --------------------------
# Home Page
# --------------------------
@main.route("/")
@login_required
def index():
    """
    Redirects to upload page after login.
    """
    return redirect(url_for("main.upload_file"))


# --------------------------
# Upload File Route
# --------------------------
@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():
    """
    Handles file upload and displays uploaded files.
    """
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part in request")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)  # Sanitize filename
            blob_client = container_client.get_blob_client(filename)
            blob_client.upload_blob(file, overwrite=True)  # Upload to Azure
            flash("File uploaded successfully!")

            return redirect(url_for("main.upload_file"))

    # Always list blobs to display in UI
    blobs = list_blobs()
    return render_template("index.html", blobs=blobs)


# --------------------------
# View File Route
# --------------------------
@main.route("/view/<filename>")
@login_required
def view_file(filename):
    """
    Generates SAS URL to view file in browser.
    """
    sas_url = get_sas_view_url(filename)
    return redirect(sas_url)


# --------------------------
# Download File Route
# --------------------------
@main.route("/download/<filename>")
@login_required
def download_file(filename):
    """
    Downloads file from Azure storage.
    """
    file_stream, mime_type = get_file_stream(filename)
    return send_file(
        BytesIO(file_stream),
        as_attachment=True,
        download_name=filename,
        mimetype=mime_type
    )


# --------------------------
# Delete File Route
# --------------------------
@main.route("/delete/<filename>", methods=["POST"])
@login_required
def delete_file(filename):
    """
    Deletes a file from Azure storage.
    """
    delete_blob(filename)
    flash(f"{filename} deleted successfully!")
    return redirect(url_for("main.upload_file"))


# --------------------------
# Logout Route
# --------------------------
@main.route("/logout")
@login_required
def logout():
    """
    Clears only user info from session and logs out.
    Avoids session.clear() to prevent wiping important data.
    """
    session.pop("user", None)  # Remove only user-related session data
    return redirect(url_for("auth.logout"))  # Redirect to Azure logout
