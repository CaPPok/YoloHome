from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 1. Tải các biến môi trường từ file .env
load_dotenv()

# 2. Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)

# 3. Cấu hình kết nối Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# 4. Khởi tạo SQLAlchemy
from models import db
db.init_app(app)

# 5. Đăng ký authentication routes
from routes.auth import auth_bp
app.register_blueprint(auth_bp)

# Đăng ký route devices
from routes.devices import devices_bp
app.register_blueprint(devices_bp)

# Đăng ký route sensors
from routes.sensors import sensors_bp
app.register_blueprint(sensors_bp)

# Đăng ký webhook Adafruit
from routes.adafruit_webhook import webhook_bp
app.register_blueprint(webhook_bp)

# ==========================================
# Home route
# ==========================================
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "YOLO-HOME Backend API"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)