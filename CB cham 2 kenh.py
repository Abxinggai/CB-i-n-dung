"""
🚀 UNDER-DESK SPOTIFY CONTROLLER V9 (Final)
HDSD:
  Kênh A (Nhạc): 1-Play/Pause | 2-Back | 3-Mute | 4-Sang Kênh B | Giữ 1s-Next
  Kênh B (Hệ thống): 1-Vol Up | 2-Vol Down | 3-Incognito Web | 4-Về Kênh A | Giữ 1s-Win+L (Lock)
Note: Chạy quyền Administrator để các lệnh hệ thống hoạt động.
"""

import serial, json, time, os, pyautogui, subprocess, sys, ctypes

# --- CẤU HÌNH ---
COM_PORT = 'COM5'
BAUD = 115200
THRESHOLD = {'A': 4000, 'B': 6000}
ID_PLAYLIST = "37i9dQZF1DXcBWIGoYBMm1"
SECRET_URL = "https://www.google.com"

pyautogui.FAILSAFE = False

def trigger(act, ser):
    print(f"Action: {act}")
    # Logic Mở Spotify
    if act.startswith("A") and act != "GO_TO_B" and "spotify.exe" not in subprocess.getoutput('tasklist').lower():
        os.startfile(f"spotify:playlist:{ID_PLAYLIST}")
        time.sleep(7); pyautogui.press('playpause'); return

    # Mapping lệnh
    cmds = {
        "A1": lambda: pyautogui.press('playpause'),
        "A2": lambda: pyautogui.press('prevtrack'),
        "A3": lambda: pyautogui.press('volumemute'),
        "AHOLD": lambda: pyautogui.press('nexttrack'),
        "GO_TO_B": lambda: ser.write(b'B'),
        "B1": lambda: pyautogui.press('volumeup'),
        "B2": lambda: pyautogui.press('volumedown'),
        "B3": lambda: subprocess.Popen(f"start msedge --inprivate {SECRET_URL}", shell=True),
        "BHOLD": lambda: ctypes.windll.user32.LockWorkStation(),
        "GO_TO_A": lambda: ser.write(b'A')
    }
    if act in cmds: cmds[act]()

def connect():
    try:
        s = serial.Serial(COM_PORT, BAUD, timeout=0.1)
        s.reset_input_buffer()
        return s
    except: return None

# --- MAIN LOOP ---
ser = connect()
t_start = time.time() if not ser else None
is_t = False; st_t = 0; count = 0; last_rel = 0; hold_ok = False; cur_m = "A"

while True:
    now = time.time()
    if ser is None or not ser.is_open:
        if t_start is None: t_start = now
        if now - t_start > 30: sys.exit() # Timeout 30s
        ser = connect()
        if ser: ser.write(b'A'); t_start = None
        else: time.sleep(1); continue

    lvl = 0
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line.startswith('{'):
                data = json.loads(line)
                cur_m, lvl = data.get("M", "A"), data.get("L", 0)
    except: ser = None; continue

    # Logic Chạm
    if lvl >= THRESHOLD[cur_m]:
        if not is_t: is_t = True; st_t = now; hold_ok = False
        if not hold_ok and (now - st_t) >= 1.0:
            trigger(cur_m + "HOLD", ser); hold_ok = True; count = 0
    else:
        if is_t:
            dur = now - st_t
            is_t = False
            if not hold_ok and dur > 0.05:
                count += 1; last_rel = now
            hold_ok = False

    if count > 0 and not is_t and (now - last_rel) > 0.6:
        tag = "GO_TO_B" if (cur_m=='A' and count>=4) else "GO_TO_A" if (cur_m=='B' and count>=4) else f"{cur_m}{count}"
        trigger(tag, ser)
        count = 0; ser.reset_input_buffer()

    time.sleep(0.01)
