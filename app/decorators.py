# app/decorators.py

from functools import wraps
from flask import redirect, url_for, session
from app.auth import get_token_from_cache

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = get_token_from_cache()
        if not token:
            return redirect(url_for("auth.login"))
        session["user"] = token.get("id_token_claims")
        return f(*args, **kwargs)
    return wrapper
