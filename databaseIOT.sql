-- 1. Bảng người dùng cơ bản
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- 2. Bảng người dùng chi tiết
CREATE TABLE nguoi_dung (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    mat_khau VARCHAR(255) NOT NULL,
    ho_va_ten VARCHAR(255) NOT NULL,
    vai_tro VARCHAR(50) DEFAULT 'user',
    du_lieu_khuon_mat TEXT,
    trang_thai_cap_quyen BOOLEAN DEFAULT TRUE
);

-- 3. Bảng nhà
CREATE TABLE nha (
    id VARCHAR(50) PRIMARY KEY,
    ten_nha VARCHAR(255) NOT NULL,
    adafruit_username VARCHAR(255),
    adafruit_key VARCHAR(255)
);

-- 4. Bảng phân quyền người dùng - nhà (Nhiều - Nhiều)
CREATE TABLE nguoi_dung_nha (
    user_id INT REFERENCES nguoi_dung(id) ON DELETE CASCADE,
    nha_id VARCHAR(50) REFERENCES nha(id) ON DELETE CASCADE,
    vai_tro_trong_nha VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, nha_id)
);

-- 5. Bảng thiết bị chung
CREATE TABLE thiet_bi (
    id VARCHAR(50) PRIMARY KEY,
    nha_id VARCHAR(50) REFERENCES nha(id) ON DELETE CASCADE,
    ten_thiet_bi VARCHAR(255) NOT NULL,
    loai_thiet_bi VARCHAR(50) NOT NULL,
    nha_san_xuat VARCHAR(255),
    vi_tri_lap_dat VARCHAR(255),
    ngay_kich_hoat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Bảng trạng thái thiết bị (Dành cho Đèn, Quạt)
CREATE TABLE trang_thai_thiet_bi (
    thiet_bi_id VARCHAR(50) PRIMARY KEY REFERENCES thiet_bi(id) ON DELETE CASCADE,
    trang_thai_bat_tat BOOLEAN DEFAULT FALSE,
    toc_do INT DEFAULT 0,
    mau_sac VARCHAR(50) DEFAULT '#FFFFFF'
);

-- 7. Bảng đặt lịch tự động
CREATE TABLE lich_trinh (
    id SERIAL PRIMARY KEY,
    thiet_bi_id VARCHAR(50) REFERENCES thiet_bi(id) ON DELETE CASCADE,
    thoi_gian_hen TIME NOT NULL,
    ngay_trong_tuan VARCHAR(100),
    trang_thai_thiet_bi_muon_dat VARCHAR(50),
    trang_thai_kich_hoat BOOLEAN DEFAULT TRUE
);

-- 8. Bảng lịch sử thao tác của người dùng
CREATE TABLE lich_su_hoat_dong (
    id SERIAL PRIMARY KEY,
    thiet_bi_id VARCHAR(50) REFERENCES thiet_bi(id) ON DELETE CASCADE,
    user_id INT REFERENCES nguoi_dung(id) ON DELETE SET NULL,
    hanh_dong VARCHAR(255) NOT NULL,
    thong_so_thay_doi VARCHAR(255),
    thoi_gian TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Bảng lịch sử tiêu thụ điện
CREATE TABLE lich_su_tieu_thu_dien (
    id SERIAL PRIMARY KEY,
    thiet_bi_id VARCHAR(50) REFERENCES thiet_bi(id) ON DELETE CASCADE,
    dien_nang_tieu_thu FLOAT NOT NULL, 
    thoi_gian_ghi_nhan TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

CREATE INDEX idx_tieu_thu_thiet_bi ON lich_su_tieu_thu_dien(thiet_bi_id);
CREATE INDEX idx_tieu_thu_thoi_gian ON lich_su_tieu_thu_dien(thoi_gian_ghi_nhan);

-- 10. Bảng Trạng thái cảm biến: CHỈ LƯU GIÁ TRỊ MỚI NHẤT
CREATE TABLE trang_thai_cam_bien (
    thiet_bi_id VARCHAR(50) PRIMARY KEY REFERENCES thiet_bi(id) ON DELETE CASCADE,
    nhiet_do FLOAT, 
    do_am FLOAT,    
    thoi_gian_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Bảng Lịch sử cảm biến (Đã gộp chung nhiệt độ, độ ẩm và giá trị khác)
CREATE TABLE lich_su_cam_bien (
    id SERIAL PRIMARY KEY,
    thiet_bi_id VARCHAR(50) REFERENCES thiet_bi(id) ON DELETE CASCADE,
    nhiet_do FLOAT,
    do_am FLOAT,
    gia_tri FLOAT, -- Giữ lại để lưu các giá trị như ánh sáng
    thoi_gian_ghi_nhan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cam_bien_thoi_gian ON lich_su_cam_bien(thoi_gian_ghi_nhan);
CREATE INDEX idx_cam_bien_thiet_bi ON lich_su_cam_bien(thiet_bi_id);