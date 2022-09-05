#include <SPI.h>
#include <RF24.h>

// ce, csn pins
RF24 radio(9, 10);

#define LED 8

// motor control for left side of robot
const int ENA = 5;
const int IN1 = 1;
const int IN2 = 2;

// motor control for right side of robot
const int ENB = 6;
const int IN3 = 3;
const int IN4 = 4;

void setup() {
  pinMode(LED, OUTPUT);
  // setting all motor driver pins
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  const uint64_t pipe = 0xE8E8F0F0E1LL;
  radio.openReadingPipe(1, pipe);
  
  radio.enableDynamicPayloads();
  radio.powerUp();

}

void loop() {
  radio.startListening();
  Serial.println("Starting loop. Radio on.");
  char receivedMessage[32] = {0};
  if (radio.available()) {
    digitalWrite(LED, HIGH);
    radio.read(receivedMessage, sizeof(receivedMessage));
    Serial.println(receivedMessage);
    Serial.println("Turning off the radio.");
    radio.stopListening();
    digitalWrite(LED, LOW);
    String stringMessage(receivedMessage);

    if (stringMessage == "FORWARD") {
      Serial.print("Moving Deliveroid FORWARD");
      const char text[] = "MOVING FORWARD";
      radio.write(text, sizeof(text));
      motorForward();
      Serial.println("Command Completed.");
    } else if (stringMessage == "REVERSE") {
      Serial.print("Moving Deliveroid REVERSE");
      const char text[] = "MOVING REVERSE";
      radio.write(text, sizeof(text));
      motorReverse();
      Serial.println("Command Completed");
    } else if (stringMessage == "RIGHT") {
      Serial.print("Moving Deliveroid RIGHT");
      const char text[] = "MOVING RIGHT";
      radio.write(text, sizeof(text));
      motorRight();
      Serial.println("Command Completed");
    } else if (stringMessage == "LEFT") {
      Serial.print("Moving Deliveroid LEFT");
      const char text[] = "MOVING LEFT";
      radio.write(text, sizeof(text));
      motorLeft();
      Serial.println("Command Completed");
    } else if (stringMessage == "STOP") {
      Serial.print("Stopping Deliveroid");
      const char text[] = "STOP";
      radio.write(text, sizeof(text));
      motorStop();
      Serial.println("Command Completed");
    }
  }

  delay(100);
}


void motorForward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}

void motorReverse() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}

void motorRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 200);
}

void motorLeft() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 200);
  analogWrite(ENB, 0);
}

void motorStop() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
