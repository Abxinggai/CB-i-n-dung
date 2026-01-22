# =================================================================
# 📘 HDSD HỆ THỐNG ĐIỀU KHIỂN GẦM BÀN V9 (Final Lock Edition):
# Chắc là đồng
# 🟢 TẦNG A (Miếng đồng bên A - GIẢI TRÍ):
#   - 1 chạm: Dừng / Phát nhạc (Play/Pause).
#   - 2 chạm: Quay lại bài trước đó (Previous Track).
#   - 3 chạm: Tắt / Bật tiếng hệ thống (Mute/Unmute).
#   - 4 chạm: CHUYỂN SANG TẦNG B (Hệ thống).
#   - Giữ 1s: Chuyển bài tiếp theo (Next Track).
#
# 🔴 TẦNG B (Miếng đồng bên B - HỆ THỐNG):
#   - 1 chạm: Tăng âm lượng (Volume Up).
#   - 2 chạm: Giảm âm lượng (Volume Down).
#   - 3 chạm: Mở Web Bí mật (Tab ẩn danh trình duyệt Edge).
#   - 4 chạm: QUAY LẠI TẦNG A (Giải trí).
#   - Giữ 1s: KHÓA MÀN HÌNH MÁY TÍNH (Win + L).
#
# ⚡ LƯU Ý: 
#   - Phải chạy phần mềm với quyền ADMINISTRATOR.
#   - Nếu Spotify chưa mở, chạm bất kỳ ở Tầng A sẽ tự khởi động Playlist.
#   - Nếu rút Arduino, code đợi 30s để bạn cắm lại trước khi tự đóng.
# =================================================================

import serial,json,time,os,pyautogui,subprocess,sys,ctypes

# --- CẤU HÌNH HỆ THỐNG ---
COM_PORT = 'COM5'
BAUD_RATE = 115200
THRESHOLD_A = 4000
THRESHOLD_B = 6000 
SECRET_URL = "ihentai.to" # Web bí mật của bạn
PLAYLIST_ID = "37i9dQZF1DXcBWIGoYBMm1" # <--- CHỈ ĐỂ MÃ ID PLAYLIST
DISCONNECT_TIMEOUT = 30 
TAP_WINDOW = 0.6          
LONG_PRESS_TIME = 3.0     

# Vô hiệu hóa bảo vệ góc màn hình
pyautogui.FAILSAFE = False

def is_spotify_running():
    """Kiểm tra xem Spotify có đang chạy hay không"""
    process = subprocess.getoutput('tasklist /FI "IMAGENAME eq Spotify.exe"')
    return "spotify.exe" in process.lower()

def trigger_action(action, ser):
    """Thực thi các lệnh điều khiển máy tính"""
    print(f"\n🎬 [HÀNH ĐỘNG]: {action}")
    
    # 1. Logic tự mở Spotify nếu chưa có
    if action.startswith("A") and action != "GO_TO_B" and not is_spotify_running():
        print(f"🚀 Khởi động Spotify Playlist: {PLAYLIST_ID}")
        # Dùng os.startfile để gọi đúng giao thức Spotify trên Windows
        os.startfile(f"spotify:playlist:{PLAYLIST_ID}")
        time.sleep(7) # Đợi App load xong 300 bài
        pyautogui.press('playpause')
        return

    # 2. Xử lý các lệnh TẦNG A
    if action == "A1": pyautogui.press('playpause')
    elif action == "A2": pyautogui.press('prevtrack')
    elif action == "A3": pyautogui.press('volumemute')
    elif action == "AHOLD": pyautogui.press('nexttrack')
    elif action == "GO_TO_B":
        print("🔑 Đã sang TẦNG B (Hệ thống)"); ser.write(b'B')

    # 3. Xử lý các lệnh TẦNG B
    elif action == "B1": pyautogui.press('volumeup')
    elif action == "B2": pyautogui.press('volumedown')
    elif action == "B3": 
        print("🕵️‍♂️ Mở Tab ẩn danh..."); subprocess.Popen(f"start msedge --inprivate {SECRET_URL}", shell=True)
    elif action == "BHOLD":
        print("🔒 Đang khóa máy (Win + L)...")
        ser.write(b'A') # Luôn đưa về A trước khi khóa để khi mở ra dùng nhạc luôn
        time.sleep(0.2)
        ctypes.windll.user32.LockWorkStation()
    elif action == "GO_TO_A":
        print("🎵 Đã về TẦNG A (Nhạc)"); ser.write(b'A')

def connect_serial():
    """Hàm kết nối Serial an toàn"""
    try:
        s = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
        s.reset_input_buffer()
        return s
    except:
        return None

# --- KHỞI CHẠY ---
ser = connect_serial()
disconnect_start_time = None if ser else time.time()
current_level = 0; current_mode = "A"
is_touching = False; touch_start_time = 0; touch_count = 0; last_rel_time = 0; hold_triggered = False

print("--- 🚀 Đa tác vụ UIA make by Ẩn ---")

try:
    while True:
        curr_time = time.time()

        # 1. QUẢN LÝ KẾT NỐI (RECONNECT & TIMEOUT)
        if ser is None or not ser.is_open:
            if disconnect_start_time is None:
                disconnect_start_time = curr_time
                print("\n🔌 Mất kết nối! Đang đợi bạn cắm lại dây R3...")

            elapsed = curr_time - disconnect_start_time
            if elapsed > DISCONNECT_TIMEOUT:
                print("\n❌ Quá 30s không thấy Arduino. Chương trình tự đóng để bảo vệ tài nguyên.")
                sys.exit()
            
            ser = connect_serial()
            if ser:
                print("\n✅ Đã kết nối lại thành công!")
                ser.write(b'A') # Khởi tạo lại Kênh A
                disconnect_start_time = None
            else:
                time.sleep(1); continue

        # 2. ĐỌC DỮ LIỆU SẠCH (CHỐNG DÍNH LẸO)
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith('{') and line.endswith('}'):
                    data = json.loads(line)
                    current_mode = data.get("M", "A")
                    current_level = data.get("L", 0)
        except:
            ser.close(); ser = None; continue

        # 3. LOGIC NHẬN DIỆN CHẠM ĐA TẦNG
        target_threshold = THRESHOLD_B if current_mode == "B" else THRESHOLD_A

        if current_level >= target_threshold:
            if not is_touching:
                is_touching = True; touch_start_time = curr_time; hold_triggered = False
                print(f"☝️  Chạm {current_mode}...")
            
            # Xử lý HOLD (Giữ lâu)
            if not hold_triggered and (curr_time - touch_start_time) >= LONG_PRESS_TIME:
                trigger_action(f"{current_mode}HOLD", ser)
                hold_triggered = True; touch_count = 0
        else:
            if is_touching:
                dur = curr_time - touch_start_time
                is_touching = False
                # Chỉ tính nhịp đập nếu là nhấp nhả
                if not hold_triggered and dur > 0.05:
                    touch_count += 1
                    last_rel_time = curr_time
                hold_triggered = False
                current_level = 0 # Xóa bộ nhớ sau nhấc tay

        # 4. CHỐT LỆNH DỰA TRÊN SỐ LẦN CHẠM
        if touch_count > 0 and not is_touching:
            if (curr_time - last_rel_time) > TAP_WINDOW:
                action_key = f"{current_mode}{touch_count}"
                # Xử lý các lệnh chuyển vùng
                if current_mode == "A" and touch_count >= 4: action_key = "GO_TO_B"
                elif current_mode == "B" and touch_count >= 4: action_key = "GO_TO_A"
                
                trigger_action(action_key, ser)
                touch_count = 0
                ser.reset_input_buffer()

        time.sleep(0.01)

except KeyboardInterrupt:
    if ser: ser.close()
    sys.exit()
