#include "HX711.h"

const int DT_PIN = 4;
const int SCK_PIN = 5;
HX711 scale;

long smart_offset = 0;
float alpha_baseline = 0.01; // Tốc độ bám sàn cực chậm

// Cấu hình bộ lọc làm mượt
const int SAMPLES = 5; // Lấy trung bình 5 lần đọc để hết nhấp nhô
long buffer[SAMPLES];
int buffer_idx = 0;

void setup() {
  Serial.begin(31250); 
  scale.begin(DT_PIN, SCK_PIN);
  scale.set_gain(128); 

  delay(5000); 

  if (scale.is_ready()) {
    smart_offset = scale.read();
    // Khởi tạo buffer bằng giá trị ban đầu
    for(int i=0; i<SAMPLES; i++) buffer[i] = smart_offset;
  }
}

void loop() {
  if (scale.is_ready()) {
    long raw = scale.read();

    // 1. Cập nhật mốc sàn thông minh (chống trôi dạt)
    long diff_to_base = raw - smart_offset;
    if (abs(diff_to_base) < 1500) {
       smart_offset = (smart_offset * (1.0 - alpha_baseline)) + (raw * alpha_baseline);
    }

    // 2. Bộ lọc Trung bình trượt (Làm mượt nhấp nhô)
    buffer[buffer_idx] = raw;
    buffer_idx = (buffer_idx + 1) % SAMPLES;

    long sum = 0;
    for(int i=0; i<SAMPLES; i++) sum += buffer[i];
    long averaged_raw = sum / SAMPLES;

    // 3. Tính Level cuối cùng (Đã làm mượt)
    long final_level = abs(averaged_raw - smart_offset);

    // 4. Gửi JSON
    Serial.print("{");
    Serial.print("\"Level\":"); 
    Serial.print(final_level);
    Serial.println("}");
  }
 
}