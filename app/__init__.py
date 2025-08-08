from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    # Required for server-side session
    app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE", "filesystem")
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Init session
    Session(app)

    return app
