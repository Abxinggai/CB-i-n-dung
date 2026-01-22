#include "HX711.h"
HX711 scale;

char mode = 'A'; // Mặc định
long offsetA = 0, offsetB = 0;

void setup() {
  Serial.begin(115200);
  scale.begin(4, 5);
  scale.set_gain(128); delay(00); offsetA = scale.read();
  scale.set_gain(32);  delay(00); offsetB = scale.read();
  scale.set_gain(128); // Quay lại A
}

void loop() {
  if (Serial.available() > 0) {
    char incoming = Serial.read();
    if (incoming == 'A' || incoming == 'B') {
      mode = incoming;
      if (mode == 'A') scale.set_gain(128); else scale.set_gain(32);
      while(!scale.is_ready()); scale.read(); // Đọc nháp để chuyển kênh
    }
  }

  if (scale.is_ready()) {
    long raw = scale.read();
    if (mode == 'A') {
      long valA = abs(raw - offsetA);
      if (valA < 4000) valA = 0;
      Serial.print("{\"M\":\"A\",\"L\":"); Serial.print(valA); Serial.println("}");
    } else {
      long valB = abs(raw - offsetB);
      if (valB < 4000) valB = 0;
      Serial.print("{\"M\":\"B\",\"L\":"); Serial.print(valB); Serial.println("}");
    }
  }
}
