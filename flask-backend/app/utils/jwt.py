import jwt
import datetime
from flask import current_app

# Generate JWT token
def encode_auth_token(user_email):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12),
            'iat': datetime.datetime.utcnow(),
            'user': user_email
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        return str(e)

# Decode JWT token
def decode_auth_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
