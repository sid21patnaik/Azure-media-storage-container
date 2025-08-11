import os
import msal
from flask import Blueprint, redirect, request, session, url_for

auth_bp = Blueprint("auth", __name__)

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = ["User.Read"]

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=cache
    )

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

@auth_bp.route("/login")
def login():
    session.clear()
    msal_app = _build_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        SCOPES,
        redirect_uri=REDIRECT_URI,
        prompt="login"
    )
    return redirect(auth_url)

@auth_bp.route("/getAToken")
def authorized():
    cache = _load_cache()
    msal_app = _build_msal_app(cache)
    code = request.args.get("code")
    if not code:
        return redirect(url_for("auth.login"))

    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    if "id_token_claims" in result:
        session["user"] = {
            "name": result["id_token_claims"].get("name"),
            "email": result["id_token_claims"].get("preferred_username"),
        }
        _save_cache(cache)
        print(f"✅ Auth success. User: {session['user']}")
        return redirect(url_for("main.upload_file"))
    else:
        print(f"❌ Auth failed: {result.get('error_description')}")
        return f"Login failed: {result.get('error_description')}", 401

@auth_bp.route("/logout")
def logout():
    session.clear()
    logout_url = f"{AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={url_for('main.upload_file', _external=True)}"
    return redirect(logout_url)
