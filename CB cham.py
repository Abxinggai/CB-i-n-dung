import serial
import json
import subprocess
import time

# --- CẤU HÌNH ---
COM_PORT = 'COM5'  
BAUD_RATE = 31250
THRESHOLD = 3000
URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# --- CHỌN TRÌNH DUYỆT CỦA BẠN ---
# Cách dùng: Bỏ dấu # ở dòng trình duyệt bạn muốn dùng

# Đối với Microsoft Edge (Mặc định trên Windows LTSC)
BROWSER_COMMAND = ["start", "msedge", URL]

# Đối với Google Chrome
# BROWSER_COMMAND = ["start", "chrome", "--incognito", URL]

# Đối với Firefox
# BROWSER_COMMAND = ["start", "firefox", "--private-window", URL]

def open_incognito():
    print(f"🚀 Bí mật mở tab ẩn danh: {URL}")
    # shell=True để chạy lệnh 'start' của Windows
    subprocess.Popen(BROWSER_COMMAND, shell=True)

while True:
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) 
        
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    data = json.loads(line)
                    level = abs(data.get("Level", 0))

                    if level >= THRESHOLD:
                        open_incognito()
                        # Đợi 5 giây để tránh mở hàng loạt tab khi vẫn đang chạm
                        time.sleep(5) 
                        ser.reset_input_buffer() 
                except:
                    continue
            time.sleep(0.01)

    except Exception:
        time.sleep(5)
        continue