#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CommandTrigger 8
#define ChannelBuffer 7

// ce, csn pins
RF24 radio(9, 10);

// motor control for left side of robot
const int ENA = 5;
const int IN1 = 1;
const int IN2 = 2;

// motor control for right side of robot
const int ENB = 6;
const int IN3 = 3;
const int IN4 = 4;

void motorForward();
void motorReverse();
void motorRight();
void motorLeft();
void motorStop();

void setup()
{
  // setting all motor driver pins
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(CommandTrigger, OUTPUT);
  pinMode(ChannelBuffer, OUTPUT);

  // beginning serial connection to radio signal

  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x70);
  radio.setDataRate(RF24_2MBPS);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  const uint64_t pipe = 0xE8E8F0F0E1LL;
  radio.openReadingPipe(1, pipe);

  radio.enableDynamicPayloads();
  radio.setRetries(0, 15);
  radio.setAutoAck(true);
  radio.powerUp();
}

void loop()
{
  digitalWrite(ChannelBuffer, HIGH);
  radio.startListening();
  Serial.println("Starting loop. Radio on.");
  char receivedMessage[32] = {0};
  if (radio.available())
  {
    digitalWrite(ChannelBuffer, HIGH);
    radio.read(receivedMessage, sizeof(receivedMessage));
    Serial.println(receivedMessage);
    Serial.println("Turning off the radio.");
    radio.stopListening();

    String stringMessage(receivedMessage);

    if (stringMessage == "FORWARD")
    {
      digitalWrite(ChannelBuffer, LOW);
      digitalWrite(CommandTrigger, HIGH);
      Serial.print("Moving Deliveroid FORWARD");
      const char text[] = "MOVING FORWARD";
      radio.write(text, sizeof(text));
      motorForward();
      Serial.println("Command Completed.");
      digitalWrite(CommandTrigger, LOW);
    }
    else if (stringMessage == "REVERSE")
    {
      digitalWrite(CommandTrigger, LOW);
      digitalWrite(CommandTrigger, HIGH);
      Serial.print("Moving Deliveroid REVERSE");
      const char text[] = "MOVING REVERSE";
      radio.write(text, sizeof(text));
      motorReverse();
      Serial.println("Command Completed");
      digitalWrite(CommandTrigger, LOW);
    }
    else if (stringMessage == "RIGHT")
    {
      digitalWrite(CommandTrigger, LOW);
      digitalWrite(CommandTrigger, HIGH);
      Serial.print("Moving Deliveroid RIGHT");
      const char text[] = "MOVING RIGHT";
      radio.write(text, sizeof(text));
      motorRight();
      Serial.println("Command Completed");
      digitalWrite(CommandTrigger, LOW);
    }
    else if (stringMessage == "LEFT")
    {
      digitalWrite(CommandTrigger, LOW);
      digitalWrite(CommandTrigger, HIGH);
      Serial.print("Moving Deliveroid LEFT");
      const char text[] = "MOVING LEFT";
      radio.write(text, sizeof(text));
      motorLeft();
      Serial.println("Command Completed");
      digitalWrite(CommandTrigger, LOW);
    }
    else if (stringMessage == "STOP")
    {
      digitalWrite(CommandTrigger, LOW);
      digitalWrite(CommandTrigger, HIGH);
      Serial.print("Stopping Deliveroid");
      const char text[] = "STOP";
      radio.write(text, sizeof(text));
      motorStop();
      Serial.println("Command Completed");
      digitalWrite(CommandTrigger, LOW);
    }
  }
}

void motorForward()
{
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}

void motorReverse()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 200);
  analogWrite(ENB, 200);
}

void motorLeft()
{
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 200);
}

void motorRight()
{
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 200);
  analogWrite(ENB, 0);
}

void motorStop()
{
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}
