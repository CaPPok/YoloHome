"""
Serial Bridge - Kết nối YOLO:BIT (USB) ↔ Flask Server
Chạy trên laptop để relay dữ liệu giữa mạch và server
"""

import serial
import requests
import json
import threading
from queue import Queue
from time import sleep
import sys

# ========== CẤU HÌNH ==========
SERIAL_PORT = "COM3"  # TODO: Sửa thành COM port của YOLO:BIT (COM3, COM4, ... COM8)
BAUD_RATE = 115200   # TODO: Kiểm tra baud rate của firmware YOLO:BIT (thường là 115200 hoặc 9600)
SERVER_URL = "http://localhost:5000"
DEVICE_ID = "yolo-bit-01"
POLL_INTERVAL = 2  # Lấy lệnh từ server mỗi 2 giây


class YoloBitBridge:
    def __init__(self):
        self.ser = None
        self.is_running = False
        self.last_control = None
        self.connect_serial()
    
    def connect_serial(self):
        """Kết nối USB serial với YOLO:BIT"""
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            # Clear buffer
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print(f"✓ Kết nối thành công: {SERIAL_PORT} @ {BAUD_RATE} baud")
            self.is_running = True
        except serial.SerialException as e:
            print(f"✗ Lỗi kết nối serial: {e}")
            print(f"   Kiểm tra lại:")
            print(f"   - YOLO:BIT đã plug vào USB chưa?")
            print(f"   - Driver CH341 đã install?")
            print(f"   - COM port {SERIAL_PORT} đúng không?")
            sys.exit(1)
    
    def read_from_device(self):
        """Đọc dữ liệu từ YOLO:BIT qua serial"""
        try:
            if self.ser and self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        data = json.loads(line)
                        return data
                    except json.JSONDecodeError:
                        print(f"  ⚠ Invalid JSON: {line}")
        except Exception as e:
            print(f"  ✗ Lỗi đọc serial: {e}")
        return None
    
    def send_to_device(self, command):
        """Gửi lệnh điều khiển tới YOLO:BIT qua serial"""
        try:
            if self.ser:
                cmd_str = json.dumps(command) + '\n'
                self.ser.write(cmd_str.encode('utf-8'))
                print(f"  → Gửi tới mạch: {command}")
                return True
        except Exception as e:
            print(f"  ✗ Lỗi gửi serial: {e}")
        return False
    
    def send_to_server(self, sensor_data):
        """Gửi dữ liệu cảm biến tới Flask server"""
        try:
            resp = requests.post(
                f"{SERVER_URL}/api/cam-bien",
                json=sensor_data,
                timeout=5
            )
            
            if resp.status_code == 200:
                print(f"  ✓ Server: cảm biến lưu thành công")
                return True
            else:
                print(f"  ⚠ Server: {resp.status_code} - {resp.text[:100]}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"  ✗ Không kết nối được Flask server ({SERVER_URL})")
            print(f"    Kiểm tra:")
            print(f"    - Flask server có chạy không?")
            print(f"    - Đúng localhost:5000 không?")
            return False
        except Exception as e:
            print(f"  ✗ Lỗi gửi server: {e}")
            return False
    
    def get_device_control(self):
        """Lấy lệnh điều khiển từ Flask server"""
        try:
            resp = requests.get(
                f"{SERVER_URL}/api/thiet-bi/{DEVICE_ID}/trang-thai",
                timeout=5
            )
            
            if resp.status_code == 200:
                data = resp.json()
                # Flask trả về format: {"status": "success", ...} hoặc {status_data}
                
                # Nếu có key 'data', lấy nó
                if isinstance(data, dict) and 'data' in data:
                    return data['data']
                # Nếu là object trực tiếp
                return data
            
            elif resp.status_code == 404:
                # Thiết bị chưa được tạo hoặc không có trạng thái
                return None
            else:
                print(f"  ⚠ Server: {resp.status_code}")
                return None
        
        except requests.exceptions.ConnectionError:
            # Nếu server không chạy, im lặng (đã warn ở send_to_server)
            return None
        except Exception as e:
            # print(f"  ✗ Lỗi lấy control: {e}")
            return None
    
    def run(self):
        """Main loop bridge"""
        print("\n" + "=" * 60)
        print("🌉 Serial Bridge đang chạy...")
        print("=" * 60)
        print(f"Port: {SERIAL_PORT} | Server: {SERVER_URL}")
        print(f"Device ID: {DEVICE_ID}")
        print("\nNhấn Ctrl+C để dừng\n")
        
        poll_counter = 0
        
        try:
            while self.is_running:
                # === 1. ĐỌC DỮ LIỆU TỪ YOLO:BIT ===
                sensor_data = self.read_from_device()
                if sensor_data:
                    print(f"\n← Nhận từ YOLO:BIT: {sensor_data}")
                    
                    # 2. GỬI LÊN FLASK SERVER
                    self.send_to_server(sensor_data)
                
                # === 3. LẤY LỆNH ĐIỀU KHIỂN TỪ SERVER (mỗi 2 giây) ===
                poll_counter += 1
                if poll_counter >= POLL_INTERVAL:
                    poll_counter = 0
                    control_cmd = self.get_device_control()
                    
                    if control_cmd and control_cmd != self.last_control:
                        print(f"\n← Lệnh từ server: {control_cmd}")
                        self.send_to_device(control_cmd)
                        self.last_control = control_cmd
                
                sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Dừng bridge...")
        except Exception as e:
            print(f"✗ Lỗi: {e}")
        finally:
            if self.ser:
                self.ser.close()
            print("✓ Đã đóng kết nối\n")


def list_ports():
    """Liệt kê tất cả COM ports"""
    try:
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            print("Không tìm thấy COM port nào")
            return
        
        print("\n=== Các COM ports available ===")
        for port, desc, hwid in ports:
            print(f"{port}: {desc}")
            if 'CH340' in desc or 'CH341' in desc:
                print(f"  ^ Có thể là YOLO:BIT (CH340/CH341 chip)")
        print()
    except Exception as e:
        print(f"Lỗi liệt kê port: {e}")


def main():
    import sys
    
    # Nếu user chạy với --list, chỉ liệt kê ports
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        list_ports()
        return
    
    print("\n" + "=" * 60)
    print("YOLO:BIT Serial Bridge v1.0")
    print("=" * 60)
    
    # Kiểm tra cấu hình
    print(f"\nCấu hình:")
    print(f"  COM Port: {SERIAL_PORT}")
    print(f"  Baud Rate: {BAUD_RATE}")
    print(f"  Server: {SERVER_URL}")
    print(f"  Device ID: {DEVICE_ID}")
    
    # Nếu cần thay đổi, hướng dẫn
    print(f"\nNếu COM port không đúng:")
    print(f"  1. Cắm YOLO:BIT vào USB")
    print(f"  2. Chạy: python serial_bridge.py --list")
    print(f"  3. Sửa SERIAL_PORT = 'COM...' trong script")
    
    input("\nNhấn Enter để tiếp tục...")
    
    # Khởi tạo & chạy bridge
    bridge = YoloBitBridge()
    bridge.run()


if __name__ == '__main__':
    main()
