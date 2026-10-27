// Front Right
#define FR_IN1 26
#define FR_IN2 25

// Front Left
#define FL_IN1 19
#define FL_IN2 27

// Rear Right
#define RR_IN1 23
#define RR_IN2 12

// Rear Left
#define RL_IN1 0
#define RL_IN2 15

int motorPins[8] = {
    FR_IN1, FR_IN2,
    FL_IN1, FL_IN2,
    RR_IN1, RR_IN2,
    RL_IN1, RL_IN2
};


void setup() {
    Serial.begin(115200);

    for (int i = 0; i < 8; i++) {
        pinMode(motorPins[i], OUTPUT);
        digitalWrite(motorPins[i], LOW);
    }
}

void loop() {
    for (int i = 0; i < 8; i += 2) {
        digitalWrite(motorPins[i], HIGH);
        digitalWrite(motorPins[i + 1], LOW);
        delay(1000);

        digitalWrite(motorPins[i], LOW);
        digitalWrite(motorPins[i + 1], LOW);
        delay(200);

        digitalWrite(motorPins[i], LOW);
        digitalWrite(motorPins[i + 1], HIGH);
        delay(1000);

        digitalWrite(motorPins[i], LOW);
        digitalWrite(motorPins[i + 1], LOW);
        delay(200);
    }
}