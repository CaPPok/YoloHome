from flask import Blueprint, request, jsonify
from models import db, ThietBi, Nha, TrangThaiThietBi, LichSuHoatDong
from utils.security import require_auth
import requests
import json
import os
from datetime import datetime

devices_bp = Blueprint('devices', __name__, url_prefix='/api/thiet-bi')


@devices_bp.route('', methods=['POST'])
def create_thiet_bi():
    payload = request.get_json() or {}
    required = ['id', 'nha_id', 'ten_thiet_bi', 'loai_thiet_bi']
    if not all(payload.get(k) for k in required):
        return jsonify({'status': 'error', 'message': 'Thiếu dữ liệu bắt buộc'}), 400

    nha = Nha.query.filter_by(id=payload['nha_id']).first()
    if not nha:
        return jsonify({'status': 'error', 'message': 'Không tìm thấy nhà'}), 404

    existed = ThietBi.query.filter_by(id=payload['id']).first()
    if existed:
        return jsonify({'status': 'error', 'message': 'ID thiết bị đã tồn tại'}), 400

    obj = ThietBi(
        id=payload['id'],
        nha_id=payload['nha_id'],
        ten_thiet_bi=payload['ten_thiet_bi'],
        loai_thiet_bi=payload['loai_thiet_bi'],
        nha_san_xuat=payload.get('nha_san_xuat'),
        vi_tri_lap_dat=payload.get('vi_tri_lap_dat')
    )

    try:
        db.session.add(obj)
        db.session.flush()

        state = TrangThaiThietBi(thiet_bi_id=obj.id)
        db.session.add(state)

        db.session.commit()
        db.session.refresh(obj)

        return jsonify({'status': 'success', 'message': 'Tạo thiết bị thành công', 'data': {'id': obj.id, 'ten_thiet_bi': obj.ten_thiet_bi}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@devices_bp.route('', methods=['GET'])
@require_auth
def get_all_thiet_bi():
    objs = ThietBi.query.all()
    return jsonify([{
        'id': x.id,
        'nha_id': x.nha_id,
        'ten_thiet_bi': x.ten_thiet_bi,
        'loai_thiet_bi': x.loai_thiet_bi,
        'nha_san_xuat': x.nha_san_xuat,
        'vi_tri_lap_dat': x.vi_tri_lap_dat,
        'trang_thai': x.trang_thai.to_dict() if x.trang_thai else None
    } for x in objs]), 200


@devices_bp.route('/<thiet_bi_id>', methods=['GET'])
@require_auth
def get_thiet_bi_detail(thiet_bi_id):
    obj = ThietBi.query.filter_by(id=thiet_bi_id).first()
    if not obj:
        return jsonify({'status': 'error', 'message': 'Không tìm thấy thiết bị'}), 404

    return jsonify({
        'id': obj.id,
        'nha_id': obj.nha_id,
        'ten_thiet_bi': obj.ten_thiet_bi,
        'loai_thiet_bi': obj.loai_thiet_bi,
        'vi_tri_lap_dat': obj.vi_tri_lap_dat,
        'trang_thai': obj.trang_thai.to_dict() if obj.trang_thai else None
    }), 200


@devices_bp.route('/<thiet_bi_id>/trang-thai', methods=['PUT'])
def update_trang_thai(thiet_bi_id):
    payload = request.get_json() or {}
    obj = TrangThaiThietBi.query.filter_by(thiet_bi_id=thiet_bi_id).first()
    if not obj:
        return jsonify({'status': 'error', 'message': 'Không tìm thấy trạng thái thiết bị'}), 404

    if 'trang_thai_bat_tat' in payload:
        obj.trang_thai_bat_tat = bool(payload['trang_thai_bat_tat'])
    if 'toc_do' in payload:
        obj.toc_do = payload['toc_do']
    if 'mau_sac' in payload:
        obj.mau_sac = payload['mau_sac']

    log = LichSuHoatDong(
        thiet_bi_id=thiet_bi_id,
        user_id=None,
        hanh_dong='Cập nhật trạng thái thiết bị',
        thong_so_thay_doi=str(payload)
    )

    try:
        db.session.add(log)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Cập nhật trạng thái thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


@devices_bp.route('/<thiet_bi_id>/control', methods=['POST'])
@require_auth
def control_thiet_bi(thiet_bi_id):
    """
    POST /api/thiet-bi/<thiet_bi_id>/control
    
    Gửi command tới Adafruit Cloud để điều khiển thiết bị
    
    Body:
    {
        "action": "on|off|set_rgb|set_speed",
        "brightness": 96,        [optional, for light RGB 0-255]
        "r": 255, "g": 255, "b": 255,  [optional, for light RGB]
        "speed": 50              [optional, for fan speed 0-100]
    }
    """
    try:
        payload = request.get_json() or {}
        action = payload.get('action')
        
        if not action:
            return jsonify({'status': 'error', 'message': 'Chưa cung cấp action'}), 400
        
        # Kiểm tra thiết bị tồn tại
        device = ThietBi.query.filter_by(id=thiet_bi_id).first()
        if not device:
            return jsonify({'status': 'error', 'message': 'Không tìm thấy thiết bị'}), 404
        
        # Cấu trúc command JSON để gửi tới Adafruit
        command = {
            'action': action,
            'source': 'webapp'
        }
        
        # Xử lý theo loại action
        if action == 'on':
            command['action'] = 'light_on' if device.loai_thiet_bi == 'den' else 'fan_on'
            
        elif action == 'off':
            command['action'] = 'light_off' if device.loai_thiet_bi == 'den' else 'fan_off'
            
        elif action == 'set_rgb' and device.loai_thiet_bi == 'den':
            command['action'] = 'light_rgb'
            command['r'] = payload.get('r', 255)
            command['g'] = payload.get('g', 255)
            command['b'] = payload.get('b', 255)
            command['brightness'] = payload.get('brightness', 96)
            
        elif action == 'set_speed' and device.loai_thiet_bi == 'quat':
            command['action'] = 'fan_speed'
            command['speed'] = payload.get('speed', 50)
        
        # Gửi tới Adafruit REST API
        response = send_command_to_adafruit(command)
        
        if not response['success']:
            return jsonify({'status': 'error', 'message': response['message']}), 500
        
        # Cập nhật trạng thái trong DB (optimistic update)
        state = TrangThaiThietBi.query.filter_by(thiet_bi_id=thiet_bi_id).first()
        if state:
            if action in ['on', 'light_on', 'fan_on']:
                state.trang_thai_bat_tat = True
            elif action in ['off', 'light_off', 'fan_off']:
                state.trang_thai_bat_tat = False
            elif action == 'set_rgb':
                state.mau_sac = f"{payload.get('r', 255)},{payload.get('g', 255)},{payload.get('b', 255)}"
                state.trang_thai_bat_tat = True  # Assume light turns on
            elif action == 'set_speed':
                state.toc_do = payload.get('speed', 50)
                state.trang_thai_bat_tat = True  # Assume fan turns on
            
            # Ghi lịch sử
            log = LichSuHoatDong(
                thiet_bi_id=thiet_bi_id,
                user_id=None,
                hanh_dong=f'Điều khiển thiết bị: {action}',
                thong_so_thay_doi=json.dumps(payload)
            )
            db.session.add(log)
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Gửi command tới Adafruit thành công',
            'data': {
                'thiet_bi_id': thiet_bi_id,
                'action': action,
                'adafruit_response': response.get('data', {})
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


def send_command_to_adafruit(command):
    """
    Gửi command tới Adafruit Cloud thông qua REST API
    
    POST https://io.adafruit.com/api/v2/{username}/feeds/yolohome-command/data
    Body: {"value": "<JSON_STRING>"}
    Header: X-AIO-Key: {key}
    """
    try:
        adafruit_user = os.getenv('ADAFRUIT_IO_USER')
        adafruit_key = os.getenv('ADAFRUIT_IO_KEY')
        
        if not adafruit_user or not adafruit_key:
            return {
                'success': False,
                'message': 'Chưa cấu hình Adafruit IO credentials (.env)'
            }
        
        # Build API URL
        url = f'https://io.adafruit.com/api/v2/{adafruit_user}/feeds/yolohome-command/data'
        
        # Prepare headers
        headers = {
            'Content-Type': 'application/json',
            'X-AIO-Key': adafruit_key
        }
        
        # Command value must be JSON string
        payload = {
            'value': json.dumps(command)
        }
        
        # Send POST request to Adafruit
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code in [200, 201]:
            return {
                'success': True,
                'message': 'Command sent to Adafruit successfully',
                'data': response.json()
            }
        else:
            return {
                'success': False,
                'message': f'Adafruit API error: {response.status_code} - {response.text}'
            }
    
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'message': 'Adafruit API timeout'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'message': f'Request error: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }
