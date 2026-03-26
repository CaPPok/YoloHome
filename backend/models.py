from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class NguoiDung(db.Model):
    """
    Ánh xạ tới bảng 'nguoi_dung' trong database
    """
    __tablename__ = 'nguoi_dung'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    mat_khau = db.Column(db.String(255), nullable=False)
    ho_va_ten = db.Column(db.String(255), nullable=False)
    vai_tro = db.Column(db.String(50), default='user')
    du_lieu_khuon_mat = db.Column(db.Text, nullable=True)
    trang_thai_cap_quyen = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<NguoiDung {self.email}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'ho_va_ten': self.ho_va_ten,
            'vai_tro': self.vai_tro,
            'trang_thai_cap_quyen': self.trang_thai_cap_quyen
        }


class Nha(db.Model):
    """Ánh xạ tới bảng 'nha' trong database"""
    __tablename__ = 'nha'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String(50), primary_key=True)
    ten_nha = db.Column(db.String(255), nullable=False)
    adafruit_username = db.Column(db.String(255), nullable=True)
    adafruit_key = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<Nha {self.ten_nha}>'


class ThietBi(db.Model):
    """Ánh xạ tới bảng 'thiet_bi' trong database"""
    __tablename__ = 'thiet_bi'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String(50), primary_key=True)
    nha_id = db.Column(db.String(50), db.ForeignKey('nha.id'), nullable=False)
    ten_thiet_bi = db.Column(db.String(255), nullable=False)
    loai_thiet_bi = db.Column(db.String(50), nullable=False)
    nha_san_xuat = db.Column(db.String(255), nullable=True)
    vi_tri_lap_dat = db.Column(db.String(255), nullable=True)
    ngay_kich_hoat = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ThietBi {self.ten_thiet_bi}>'
