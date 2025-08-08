import msal
import os
from flask import session, redirect, request, url_for, Blueprint

# Load configs from environment
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
REDIRECT_PATH = "/getAToken"
SCOPES = ["User.Read"]
REDIRECT_URI = os.getenv("REDIRECT_URI")

auth_bp = Blueprint("auth", __name__)

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET, token_cache=cache)

def load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

def build_auth_url():
    msal_app = _build_msal_app()
    return msal_app.get_authorization_request_url(
        SCOPES,
        redirect_uri=REDIRECT_URI,
        prompt="login"  # 👈 this line forces fresh login
    )

def get_token_from_cache():
    cache = load_cache()
    cca = _build_msal_app(cache)
    accounts = cca.get_accounts()
    if accounts:
        result = cca.acquire_token_silent(SCOPES, account=accounts[0])
        save_cache(cache)
        return result
    return None

# ✅ Login route
@auth_bp.route("/login")
def login():
    auth_url = build_auth_url()
    return redirect(auth_url)

# ✅ Redirect callback
@auth_bp.route("/getAToken")
def authorized():
    cache = load_cache()
    result = None
    
    if "code" not in request.args:
        return redirect(url_for("auth.login"))

    if request.args.get("code"):
        msal_app = _build_msal_app(cache)
        result = msal_app.acquire_token_by_authorization_code(
            request.args["code"],
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )

        if "access_token" in result:
            session["user"] = result.get("id_token_claims")
            save_cache(cache)
            print("✅ Auth success. User:", session["user"])
            return redirect(url_for("main.upload_file"))
        else:
            print("❌ Failed to get token:", result)
            return f"Login failed: {result.get('error_description')}", 401
    return "No code provided", 400


# ✅ Logout route
@auth_bp.route("/logout")
def logout():
    session.clear()
    logout_url = f"{AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={url_for('auth.login', _external=True)}"
    return redirect(logout_url)

