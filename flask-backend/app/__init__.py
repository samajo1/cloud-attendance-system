from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app
from .config import Config
import os


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Firebase initialization
    cred = credentials.Certificate(os.path.join(os.getcwd(), 'firebase_credentials.json'))
    initialize_app(cred)

    # Store db connection
    app.db = firestore.client()

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.attendance import attendance_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

    return app
