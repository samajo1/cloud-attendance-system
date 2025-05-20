from flask import Blueprint, request, jsonify, current_app
from firebase_admin import firestore
from app.utils.jwt import encode_auth_token
import bcrypt

auth_bp = Blueprint('auth', __name__)
db = firestore.client()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    if db.collection('users').document(email).get().exists:
        return jsonify({'message': 'User already exists'}), 409

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.collection('users').document(email).set({
        'email': email,
        'password': hashed_pw,
        'role': role
    })

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_doc = db.collection('users').document(email).get()
    if not user_doc.exists:
        return jsonify({'message': 'Invalid credentials'}), 401

    user = user_doc.to_dict()
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = encode_auth_token(email)
    return jsonify({'token': token}), 200


@auth_bp.route('/me', methods=['GET'])
def get_me():
    user, error = verify_token(request)
    if error:
        return jsonify({'message': error}), 401
    return jsonify(user), 200
