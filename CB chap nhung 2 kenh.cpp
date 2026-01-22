#include "HX711.h"

// Chân kết nối DT=4, SCK=5
HX711 scale;
char mode = 'A'; 
long offsetA = 0, offsetB = 0;

void setup() {
  Serial.begin(115200);
  scale.begin(4, 5);
  
  // Lấy mốc sàn ban đầu cho 2 kênh
  scale.set_gain(128); delay(500); offsetA = scale.read();
  scale.set_gain(32);  delay(500); offsetB = scale.read();
  scale.set_gain(128);
}

void loop() {
  // Nhận lệnh chuyển mode từ máy tính
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'A' || cmd == 'B') {
      mode = cmd;
      scale.set_gain(mode == 'A' ? 128 : 32);
      while(!scale.is_ready()); scale.read(); // Đọc nháp để chuyển mode
    }
  }

  // Đọc và gửi dữ liệu
  if (scale.is_ready()) {
    long raw = scale.read();
    long current_offset = (mode == 'A') ? offsetA : offsetB;
    long diff = abs(raw - current_offset);

    // Bám sàn thông minh (Deadzone 6000)
    if (diff < 6000) {
      if (mode == 'A') offsetA = (offsetA * 0.9) + (raw * 0.1);
      else offsetB = (offsetB * 0.9) + (raw * 0.1);
      diff = 0;
    }

    // Gửi JSON rút gọn: {"M":"A","L":100}
    Serial.print("{\"M\":\""); Serial.print(mode);
    Serial.print("\",\"L\":"); Serial.print(diff);
    Serial.println("}");
  }
}
