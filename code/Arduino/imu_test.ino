#include <Wire.h>

#define SDA_PIN 21
#define SCL_PIN 22
#define MPU_ADDR 0x68


void setup() {
    Serial.begin(115200);

    // I2C 시작
    Wire.begin(SDA_PIN, SCL_PIN);

    // MPU6050은 전원이 들어오면 sleep 상태이므로 먼저 깨워준다
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x6B);     // 전원 관리 레지스터(PWR_MGMT_1) 선택
    Wire.write(0x00);     // sleep 비트 해제
    Wire.endTransmission();
}

void loop() {
    // 가속도 X축 데이터가 시작되는 0x3B 레지스터부터 읽는다
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B);

    // 통신을 끊지 않고 바로 이어서 데이터를 읽기 위해 false 사용
    Wire.endTransmission(false);

    // 가속도 6바이트 + 온도 2바이트 + 자이로 6바이트
    Wire.requestFrom(MPU_ADDR, 14);

    // 필요한 14바이트를 모두 받지 못했으면 이번 측정은 건너뛴다
    if (Wire.available() < 14) {
        Serial.println("MPU6050 read failed");
        delay(100);
        return;
    }

    // 각 센서 값은 상위 8bit와 하위 8bit 두 바이트로 저장되어 있다 (총 2 Byte)
    int16_t ax_raw = (Wire.read() << 8) | Wire.read();
    int16_t ay_raw = (Wire.read() << 8) | Wire.read();
    int16_t az_raw = (Wire.read() << 8) | Wire.read();

    // 온도 데이터는 지금 사용하지 않는다 (읽어서 넘겨야 다음 자이로 데이터를 읽을 수 있음)
    int16_t temp_raw = (Wire.read() << 8) | Wire.read();

    // 자이로 데이터 (마찬가지로 2 Byte 데이터)
    int16_t gx_raw = (Wire.read() << 8) | Wire.read();
    int16_t gy_raw = (Wire.read() << 8) | Wire.read();
    int16_t gz_raw = (Wire.read() << 8) | Wire.read();


    // m/s^2으로 변환
    float ax = (ax_raw / 16384.0) * 9.80665;
    float ay = (ay_raw / 16384.0) * 9.80665;
    float az = (az_raw / 16384.0) * 9.80665;


    // deg/s로 변환
    float gx = gx_raw / 131.0;
    float gy = gy_raw / 131.0;
    float gz = gz_raw / 131.0;

    // Acclerometer 출력
    Serial.print("Accel [m/s^2]: ");
    Serial.print(ax, 3);
    Serial.print(", ");
    Serial.print(ay, 3);
    Serial.print(", ");
    Serial.print(az, 3);

    // Gyroscope 출력
    Serial.print(" | Gyro [deg/s]: ");
    Serial.print(gx, 2);
    Serial.print(", ");
    Serial.print(gy, 2);
    Serial.print(", ");
    Serial.println(gz, 2);

    delay(100);
}