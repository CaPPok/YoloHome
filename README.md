# YOLO:HOME - Smart Home Control System

## Framework
```
Frontend: Vite + React
Backend: Flask
Database: PostgreSQL
```

### Backend Setup

```bash
cd backend

''' 
1. Tạo file .env và thêm dòng code này vào
Nhập mật khẩu của pgAdmin4 vào "your_password"
Nhập tên database vào "name_database"
'''
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/name_database

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Chạy server
python app.py

# hoặc

flask run
```

Server chạy tại: **http://localhost:5000**

### Frontend Setup

```bash
cd frontend

# 1. Cài dependencies
npm install

# 2. Chạy dev server
npm run dev
```

Frontend chạy tại: **http://localhost:5173**

---

## Login

Mở **http://localhost:5173** → Nhập email + password từ database

---

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Home |
| POST | `/api/auth/login` | Login endpoint |

---

## Database Schema

Sử dụng database hiện tại tại PostgreSQL với bảng `nguoi_dung` (email, mat_khau, ho_va_ten, vai_tro, etc.)

---