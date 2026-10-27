#define BUZZER_PIN 5

#define BUZZER_FREQ 2000   // 2000 Hz
#define RESOLUTION  8      // 8-bit: duty 0~255


void setup() {
    ledcAttach(BUZZER_PIN, BUZZER_FREQ, RESOLUTION);
}

void loop() {
    // 작은 소리
    ledcWrite(BUZZER_PIN, 32);
    delay(1000);

    // 중간 소리
    ledcWrite(BUZZER_PIN, 64);
    delay(1000);

    // 큰 소리
    ledcWrite(BUZZER_PIN, 128);
    delay(1000);

    // 끄기
    ledcWrite(BUZZER_PIN, 0);
    delay(1000);
}