from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder="../templates")  # this is important!

    from .routes import main
    app.register_blueprint(main)

    return app
