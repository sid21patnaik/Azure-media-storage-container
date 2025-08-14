from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Flask-Session config
    app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE", "filesystem")
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Detect environment for secure cookies
    if os.getenv("ENVIRONMENT") == "DEV":
        app.config['SESSION_COOKIE_SECURE'] = True
    else:
        app.config['SESSION_COOKIE_SECURE'] = False

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Initialize session
    Session(app)

    # Dynamically set redirect URI for Azure deployment
    if os.getenv("ENVIRONMENT") == "DEV":
        from .auth import REDIRECT_URI as _azure_redirect_uri
        os.environ["REDIRECT_URI"] = _azure_redirect_uri

    return app
