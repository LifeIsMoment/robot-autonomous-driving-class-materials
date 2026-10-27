#include <ESP32Servo.h>

#define SERVO_PIN 14

Servo myServo;


void setup() {
    myServo.attach(SERVO_PIN);
    myServo.write(0);
}

void loop() {
    for (int angle = 0; angle <= 180; angle+=5) {
        myServo.write(angle);
        delay(15);
    }

    for (int angle = 180; angle >= 0; angle-=5) {
        myServo.write(angle);
        delay(15);
    }
}
