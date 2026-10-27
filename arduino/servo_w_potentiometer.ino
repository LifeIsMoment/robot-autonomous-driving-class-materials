#include <ESP32Servo.h>

#define POT_PIN   39
#define SERVO_PIN 14

Servo servo;


void setup() {
    Serial.begin(115200);
    servo.attach(SERVO_PIN);
}

void loop()
{
    int potValue = analogRead(POT_PIN);
    int angle = map(potValue, 0, 4095, 0, 180);

    servo.write(angle);
    delay(20);
}