/*
 * Back  :    0°
 * Left  :   90°
 * Front :  180°
 * Right :  270°
*/


#define LIDAR_RX 16

uint8_t packet[47];
uint16_t distances[360] = {0};

float previousAngle = -1.0;


// LiDAR가 low byte, high byte 순서로 보낸 2바이트를 하나의 16비트 정수로 합친다
uint16_t readUInt16(uint8_t low, uint8_t high) {
    return low | (high << 8);
}


// target 각도 주변 +/-3도 범위에서 0이 아닌 값 중 가장 가까운 거리값을 찾는다
uint16_t getDistanceAround(int target) {
    uint16_t minDistance = 0;

    for (int offset = -3; offset <= 3; offset++) {
        int angle = target + offset;

        if (angle < 0) angle += 360;
        if (angle >= 360) angle -= 360;

        uint16_t d = distances[angle];

        if (d > 0) {
            if (minDistance == 0 || d < minDistance) {
                minDistance = d;
            }
        }
    }

    return minDistance;
}


void printDirections()
{
    Serial.print("Front : ");
    Serial.print(getDistanceAround(180));
    Serial.println(" mm");

    Serial.print("Back  : ");
    Serial.print(getDistanceAround(0));
    Serial.println(" mm");

    Serial.print("Left  : ");
    Serial.print(getDistanceAround(90));
    Serial.println(" mm");

    Serial.print("Right : ");
    Serial.print(getDistanceAround(270));
    Serial.println(" mm");

    Serial.println("----------------");
}


void setup() {
    Serial.begin(115200);  // 시리얼 모니터
    Serial2.begin(230400, SERIAL_8N1, LIDAR_RX, -1);  // LiDAR -> RX 시리얼 통신 (TX 사용안함)
}


void loop() {
    if (!Serial2.available()) {
        return;
    }

    // packet의 첫 byte는 항상 0x54
    if (Serial2.read() != 0x54) {
        return;
    }

    // 두 번째 byte가 들어올 때까지 기다린다
    while (!Serial2.available()) {
    }

    // 두 번째 byte가 0x2C인지 확인
    if (Serial2.read() != 0x2C) {
        return;
    }

    packet[0] = 0x54;
    packet[1] = 0x2C;

    // header 2바이트를 제외한 나머지 packet 데이터를 읽는다 (총 47 바이트)
    for (int i = 2; i < 47; i++) {
        while (!Serial2.available()) {
        }

        packet[i] = Serial2.read();
    }

    // 시작 각도와 끝 각도는 각각 2바이트
    uint16_t startRaw = readUInt16(packet[4], packet[5]);
    uint16_t endRaw = readUInt16(packet[42], packet[43]);

    // 각도값은 0.01도 단위로 들어오므로 100으로 나눈다
    float startAngle = startRaw / 100.0;
    float endAngle = endRaw / 100.0;

    if (endAngle < startAngle) {
        endAngle += 360.0;
    }

    // 한 packet에는 12개 측정점이 있으므로 시작점과 끝점 사이를 11구간으로 나눈다.
    float angleStep = (endAngle - startAngle) / 11.0;

    for (int i = 0; i < 12; i++) {
        // 각 측정점은 distance 2바이트 + confidence 1바이트로 구성
        int index = 6 + i * 3;

        // 거리값 2바이트를 mm 단위 정수로 변환
        uint16_t distance = readUInt16(packet[index], packet[index + 1]);

        // 현재 측정점이 어느 각도에 해당하는지 계산
        float angle = startAngle + angleStep * i;

        if (angle >= 360.0) {
            angle -= 360.0;
        }

        // 이전 값이 300도 이상이고 현재 값이 60도 미만이면 360도에서 0도로 넘어온 것으로 보고 한 바퀴 완료 처리
        if (previousAngle > 300.0 && angle < 60.0) {
            printDirections();
        }

        // float 각도를 가장 가까운 정수 각도로 반올림
        int degree = (int)(angle + 0.5);

        if (degree >= 360) {
            degree = 0;
        }

        // 0은 유효하지 않은 거리값으로 보고 저장하지 않는다
        if (distance > 0) {
            distances[degree] = distance;
        }

        previousAngle = angle;
    }
}