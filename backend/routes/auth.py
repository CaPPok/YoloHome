from flask import Blueprint, request, jsonify
from models import NguoiDung
from utils.security import generate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    API Login - Query từ bảng 'nguoi_dung' trong database
    
    Body: {
        "email": "user@example.com",
        "password": "mat_khau"
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'status': 'error',
                'message': 'Email và mật khẩu không được để trống'
            }), 400
        
        email = data.get('email').strip()
        password = data.get('password')
        
        # Query người dùng từ database
        user = NguoiDung.query.filter_by(email=email).first()
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'Email hoặc mật khẩu không chính xác'
            }), 401
        
        # So sánh mật khẩu trực tiếp (không mã hóa)
        if password != user.mat_khau:
            return jsonify({
                'status': 'error',
                'message': 'Email hoặc mật khẩu không chính xác'
            }), 401
        
        # Kiểm tra quyền truy cập
        if not user.trang_thai_cap_quyen:
            return jsonify({
                'status': 'error',
                'message': 'Tài khoản của bạn chưa được cấp quyền'
            }), 403
        
        # Tạo JWT token
        token = generate_token(user.id)
        
        return jsonify({
            'status': 'success',
            'message': 'Đăng nhập thành công',
            'data': {
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'ho_va_ten': user.ho_va_ten,
                    'vai_tro': user.vai_tro
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Lỗi server: {str(e)}'
        }), 500


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    API lấy thông tin user hiện tại (dùng token)
    Header: Authorization: Bearer <token>
    """
    try:
        from utils.security import verify_token
        
        # Lấy token từ header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'status': 'error',
                'message': 'Missing authorization header'
            }), 401
        
        try:
            token = auth_header.split(' ')[1]
        except:
            return jsonify({
                'status': 'error',
                'message': 'Invalid token format'
            }), 401
        
        # Verify token
        payload = verify_token(token)
        if not payload:
            return jsonify({
                'status': 'error',
                'message': 'Token invalid hoặc hết hạn'
            }), 401
        
        # Lấy user từ database
        user = NguoiDung.query.get(payload['user_id'])
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Lỗi server: {str(e)}'
        }), 500
