from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from datetime import datetime
from app.utils.jwt import decode_auth_token

attendance_bp = Blueprint('attendance', __name__)
db = firestore.client()

def verify_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, 'Missing or invalid token'

    token = auth_header.split(' ')[1]
    email = decode_auth_token(token)
    if isinstance(email, str) and 'invalid' in email.lower():
        return None, email

    # Get user role
    user_doc = db.collection('users').document(email).get()
    if not user_doc.exists:
        return None, 'User not found'
    user_data = user_doc.to_dict()
    return {'email': email, 'role': user_data.get('role')}, None


@attendance_bp.route('/check-in', methods=['POST'])
def check_in():
    user_email, error = verify_token(request)
    if error:
        return jsonify({'message': error}), 401

    now = datetime.utcnow()
    db.collection('attendance').add({
        'email': user_email,
        'check_in': now,
        'check_out': None,
        'date': now.strftime('%Y-%m-%d')
    })
    return jsonify({'message': 'Checked in successfully', 'time': now.isoformat()}), 200

@attendance_bp.route('/check-out', methods=['POST'])
def check_out():
    user_email, error = verify_token(request)
    if error:
        return jsonify({'message': error}), 401

    today = datetime.utcnow().strftime('%Y-%m-%d')
    query = db.collection('attendance').where('email', '==', user_email).where('date', '==', today).order_by('check_in', direction=firestore.Query.DESCENDING).limit(1)
    docs = query.stream()

    updated = False
    for doc in docs:
        db.collection('attendance').document(doc.id).update({
            'check_out': datetime.utcnow()
        })
        updated = True

    if not updated:
        return jsonify({'message': 'No check-in record found for today'}),
@attendance_bp.route('/logs/all', methods=['GET'])
def get_all_logs():
    user, error = verify_token(request)
    if error:
        return jsonify({'message': error}), 401
    if user['role'] != 'admin':
        return jsonify({'message': 'Access denied'}), 403

    query = db.collection('attendance').order_by('check_in')
    logs = [
        {**doc.to_dict(), 'id': doc.id}
        for doc in query.stream()
    ]
    return jsonify({'logs': logs}), 200
