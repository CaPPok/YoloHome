import jwt
from datetime import datetime, timedelta
import os

def generate_token(user_id, expires_in=86400):
    """Tạo JWT token"""
    secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in)
    }
    
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_token(token):
    """Xác thực token"""
    try:
        secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except:
        return None
