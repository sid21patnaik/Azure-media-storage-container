# Azure Media Storage Container

**A Flask-based media storage app** that uses **Azure Blob Storage** for file storage and **Azure Entra ID (Azure AD)** for authentication. The app supports uploading, listing, viewing/downloading, and deleting files via a simple web UI and is designed for easy deployment to Azure App Service.

---

## Key features

* Upload files to an Azure Blob Storage container
* List, view (in-browser for supported types), download, and delete files
* User authentication via Azure Entra ID using MSAL
* Server-side sessions (Flask-Session)
* Deployable to Azure App Service (startup script provided)

---

## Project structure (actual)

```
Azure-media-storage-container-main/
├── app/                      # Flask app package
│   ├── __init__.py           # app factory, session setup
│   ├── auth.py               # MSAL / Azure AD auth logic
│   ├── azure_utils.py        # Azure Blob helper functions
│   ├── config.py             # (optional) config class
│   ├── routes.py             # main routes and blueprint
├── templates/                # Jinja2 templates
│   └── index.html
├── run.py                    # Launch script for local dev
├── startup.sh                # Startup command for Azure App Service
├── requirements.txt          # Python dependencies
├── README.md                 # (this file)
```

> Note: Your repo may also contain `app.py` (a single-file version) and a `flask_session/` folder with local session files — the app factory (`app/__init__.py`) and `run.py` are the canonical entry points used by the current project layout.

---

## Prerequisites

* Python 3.8+ (3.10+ recommended)
* pip
* An **Azure Storage Account** with a Blob container
* An **Azure App Registration** (Entra ID) with a client ID and client secret
* Optional: Azure App Service for deployment

---

## Environment variables

Create a `.env` file in the project root (this file should not be committed). The code references a few environment variables — some modules use slightly different names; providing both sets below avoids surprises.

```env
# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=...  # required
AZURE_STORAGE_CONTAINER_NAME=your-container-name

# Azure AD / MSAL (used by app/auth.py)
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id
REDIRECT_URI=http://localhost:5000/getAToken

# Alternate config keys (some modules use these names)
CLIENT_ID=${AZURE_CLIENT_ID}
CLIENT_SECRET=${AZURE_CLIENT_SECRET}
AUTHORITY=https://login.microsoftonline.com/${AZURE_TENANT_ID}

# Flask session config (optional)
SESSION_TYPE=filesystem

# Local dev secret (optional)
FLASK_SECRET_KEY=some-secret-value
```

> **Important:** The project contains multiple modules that may look for `AZURE_CLIENT_ID` vs `CLIENT_ID` — the `.env` above sets both so the application finds what it needs. If you prefer, standardize the environment variable names in your code and update the `.env` accordingly.

---

## Installation (local dev)

1. Clone the repo:

```bash
git clone https://github.com/sid21patnaik/Azure-media-storage-container.git
cd Azure-media-storage-container
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file as shown above and populate it with your Azure values.

5. Run the app:

```bash
# Option A: Use the run script
python run.py

# Option B: Use flask directly (set FLASK_APP=run.py)
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=5000
```

Open `http://localhost:5000` in your browser. During the first login, you will be redirected to Microsoft to authenticate, then returned to the app.

---

## How it works (high-level)

* `app/azure_utils.py` contains helpers to connect to Azure Blob Storage (`BlobServiceClient`), list blobs, upload, download, generate SAS view URLs, and stream file data.
* `app/auth.py` uses **msal** to perform the OAuth2 authorization code flow with Azure Entra ID and stores minimal user info in the session.
* `app/routes.py` (or `app.py` depending on the variant) exposes endpoints for uploading, listing, viewing/downloading, and deleting files.
* `startup.sh` runs `gunicorn` on port `8000` (required for Azure App Service Linux containers).

---

## Deployment to Azure App Service (quick)

1. Push code to a GitHub repo.
2. In VS Code (Codespaces) with the Azure extension: right-click your App Service → **Deploy to Web App** → select project root.
3. In the Azure Portal, open your Web App → **Configuration** → add the environment variables from the `.env` file.
4. Set the **Startup Command** (under Configuration → General Settings) to:

```
bash startup.sh
```

5. Ensure the App Service **Python version** matches your runtime (3.10/3.11/3.12) and **restart** the web app.

**Troubleshooting:**

* If logs say `bash: startup.sh: No such file or directory`, ensure `startup.sh` is in the repo root and was deployed (re-deploy selecting the project root).
* If logs say `didn't respond to HTTP pings on port: 8000`, confirm `startup.sh` binds to port 8000 (`gunicorn --bind=0.0.0.0:8000 ...`).
* Use **Log Stream** and **Kudu (Advanced Tools)** to inspect runtime logs and deployed files.

---

## Common troubleshooting (auth & MSAL)

* `AADSTS900144: The request body must contain the following parameter: 'client_id'` — make sure the client ID and client secret environment variables are set correctly and MSAL is reading them.
* `ValueError: You cannot use any scope value that is reserved.` — do not mix OpenID scopes (`openid`, `profile`, `offline_access`) with resource scopes like `User.Read` in the same request. Use `SCOPES = ["User.Read"]` for MS Graph access, or `SCOPES = ["openid", "profile", "email"]` for pure OIDC.
* If `session['user']` is empty, add debug prints in `auth.py` to inspect `result` returned by `acquire_token_by_authorization_code` and ensure `id_token_claims` exist.

---

## Testing

* Login: Click **Login** — you should be redirected to Microsoft login and back to the app.
* Upload: Use the upload form to post a file. The app will upload to the configured Blob container.
* List/View/Download/Delete: Use the buttons next to each listed blob.

---

## Notes & Next steps

* Consider consolidating environment variable names across modules (use a single naming convention) to avoid confusion when deploying.
* Add in-browser viewing for more file types.
* Improve UI and add pagination/search for large blob lists.

---

## License

MIT

---

If you want, I can:

* Commit/replace the existing `README.md` in your repo (I can provide the file ready to paste), or
* Open a PR with the new README if you give me repo access.

Which would you prefer?
