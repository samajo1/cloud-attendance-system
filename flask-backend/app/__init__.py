from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app
from .config import Config
import os
import base64
import json
from io import BytesIO

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Firebase initialization
    firebase_cert = os.environ.get("FIREBASE_CERT")
    if firebase_cert:
        import base64
        import json
        cert_json = base64.b64decode(firebase_cert).decode("utf-8")
        cred = credentials.Certificate(json.loads(cert_json))
        initialize_app(cred)
    else:
        raise ValueError("Missing FIREBASE_CERT environment variable")

    # Firestore client
    app.db = firestore.client()

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.attendance import attendance_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

    # ✅ Add root route here
    @app.route('/')
    def index():
        return {"message": "Attendance backend is running!"}

    return app


