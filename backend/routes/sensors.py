from flask import Blueprint, request, jsonify
from models import db, TrangThaiCamBien, LichSuCamBien, ThietBi, TrangThaiThietBi
from utils.security import require_auth
from datetime import datetime, timedelta

sensors_bp = Blueprint('sensors', __name__, url_prefix='/api/cam-bien')


@sensors_bp.route('', methods=['GET'])
@require_auth
def get_all_sensor_data():
    """
    GET /api/cam-bien
    Lấy dữ liệu cảm biến mới nhất từ tất cả cảm biến
    """
    try:
        sensors = TrangThaiCamBien.query.all()
        
        result = []
        for sensor in sensors:
            device = ThietBi.query.filter_by(id=sensor.thiet_bi_id).first()
            result.append({
                'id': sensor.thiet_bi_id,
                'thiet_bi_id': sensor.thiet_bi_id,
                'thiet_bi_ten': device.ten_thiet_bi if device else 'Unknown',
                'nhiet_do': sensor.nhiet_do,
                'do_am': sensor.do_am,
                'thoi_gian_cap_nhat': sensor.thoi_gian_cap_nhat.isoformat() if sensor.thoi_gian_cap_nhat else None
            })
        
        return jsonify({'status': 'success', 'data': result}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@sensors_bp.route('/devices', methods=['GET'])
@require_auth
def get_all_devices_with_sensors():
    """
    GET /api/cam-bien/devices
    Lấy ALL devices (LED, FAN, SENSOR) cùng trạng thái hiện tại
    """
    try:
        devices = ThietBi.query.all()
        
        result = []
        for device in devices:
            device_data = {
                'id': device.id,
                'nha_id': device.nha_id,
                'ten_thiet_bi': device.ten_thiet_bi,
                'loai_thiet_bi': device.loai_thiet_bi,
                'nha_san_xuat': device.nha_san_xuat,
                'vi_tri_lap_dat': device.vi_tri_lap_dat,
                'ngay_kich_hoat': device.ngay_kich_hoat.isoformat() if device.ngay_kich_hoat else None
            }
            
            # Thêm trạng thái nếu là device (LED, FAN)
            if device.trang_thai:
                device_data['trang_thai'] = {
                    'trang_thai_bat_tat': device.trang_thai.trang_thai_bat_tat,
                    'toc_do': device.trang_thai.toc_do,
                    'mau_sac': device.trang_thai.mau_sac
                }
            
            # Thêm sensor data nếu là cảm biến
            sensor_data = TrangThaiCamBien.query.filter_by(thiet_bi_id=device.id).first()
            if sensor_data:
                device_data['sensor'] = {
                    'nhiet_do': sensor_data.nhiet_do,
                    'do_am': sensor_data.do_am,
                    'thoi_gian_cap_nhat': sensor_data.thoi_gian_cap_nhat.isoformat() if sensor_data.thoi_gian_cap_nhat else None
                }
            
            result.append(device_data)
        
        return jsonify({'status': 'success', 'data': result}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@sensors_bp.route('/<thiet_bi_id>', methods=['GET'])
@require_auth
def get_sensor_by_device(thiet_bi_id):
    """
    GET /api/cam-bien/<thiet_bi_id>
    Lấy dữ liệu cảm biến mới nhất của một thiết bị
    """
    try:
        sensor = TrangThaiCamBien.query.filter_by(thiet_bi_id=thiet_bi_id).first()
        
        if not sensor:
            return jsonify({'status': 'error', 'message': 'Cảm biến không tìm thấy'}), 404
        
        device = ThietBi.query.filter_by(id=thiet_bi_id).first()
        
        return jsonify({
            'status': 'success',
            'data': {
                'id': sensor.thiet_bi_id,
                'thiet_bi_id': sensor.thiet_bi_id,
                'thiet_bi_ten': device.ten_thiet_bi if device else 'Unknown',
                'nhiet_do': sensor.nhiet_do,
                'do_am': sensor.do_am,
                'thoi_gian_cap_nhat': sensor.thoi_gian_cap_nhat.isoformat() if sensor.thoi_gian_cap_nhat else None
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@sensors_bp.route('/<thiet_bi_id>/lich-su', methods=['GET'])
@require_auth
def get_sensor_history(thiet_bi_id):
    """
    GET /api/cam-bien/<thiet_bi_id>/lich-su?limit=24&hours=24
    Lấy lịch sử dữ liệu cảm biến (mặc định 24 giờ gần nhất, max 100 records)
    """
    try:
        hours = request.args.get('hours', 24, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        # Tính thời gian bắt đầu
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        history = LichSuCamBien.query.filter_by(thiet_bi_id=thiet_bi_id).filter(
            LichSuCamBien.thoi_gian_ghi_nhan >= start_time
        ).order_by(LichSuCamBien.thoi_gian_ghi_nhan.desc()).limit(limit).all()
        
        if not history:
            return jsonify({
                'status': 'success',
                'data': [],
                'message': f'Không có dữ liệu từ {hours} giờ trước'
            }), 200
        
        # Reverse để hiển thị theo thứ tự thời gian tăng dần
        history.reverse()
        
        device = ThietBi.query.filter_by(id=thiet_bi_id).first()
        
        return jsonify({
            'status': 'success',
            'thiet_bi_ten': device.ten_thiet_bi if device else 'Unknown',
            'data': [{
                'id': h.id,
                'thiet_bi_id': h.thiet_bi_id,
                'nhiet_do': h.nhiet_do,
                'do_am': h.do_am,
                'thoi_gian_ghi_nhan': h.thoi_gian_ghi_nhan.isoformat() if h.thoi_gian_ghi_nhan else None
            } for h in history]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@sensors_bp.route('/<thiet_bi_id>', methods=['POST'])
def update_sensor_data(thiet_bi_id):
    """
    POST /api/cam-bien/<thiet_bi_id>
    Cập nhật dữ liệu cảm biến (ghi dữ liệu mới nhất và lưu lịch sử)
    Body: {"nhiet_do": 27.5, "do_am": 62}
    """
    payload = request.get_json() or {}
    
    device = ThietBi.query.filter_by(id=thiet_bi_id).first()
    if not device:
        return jsonify({'status': 'error', 'message': 'Thiết bị không tìm thấy'}), 404
    
    nhiet_do = payload.get('nhiet_do')
    do_am = payload.get('do_am')
    
    try:
        # Cập nhật hoặc tạo mới TrangThaiCamBien (trạng thái hiện tại)
        sensor_state = TrangThaiCamBien.query.filter_by(thiet_bi_id=thiet_bi_id).first()
        
        if sensor_state:
            sensor_state.nhiet_do = nhiet_do
            sensor_state.do_am = do_am
            sensor_state.thoi_gian_cap_nhat = datetime.utcnow()
        else:
            sensor_state = TrangThaiCamBien(
                thiet_bi_id=thiet_bi_id,
                nhiet_do=nhiet_do,
                do_am=do_am
            )
            db.session.add(sensor_state)
        
        # Lưu vào LichSuCamBien (lịch sử)
        history = LichSuCamBien(
            thiet_bi_id=thiet_bi_id,
            nhiet_do=nhiet_do,
            do_am=do_am
        )
        db.session.add(history)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Cập nhật dữ liệu cảm biến {device.ten_thiet_bi} thành công',
            'data': sensor_state.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
