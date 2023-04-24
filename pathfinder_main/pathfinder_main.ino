#include <SoftwareSerial.h>
SoftwareSerial BT(11, 10);

#define IR_LEFT 2
#define IR_RIGHT 13

#define LEFT_F 4
#define LEFT_B 5
#define LEFT_E 3
#define RIGHT_F 6
#define RIGHT_B 8
#define RIGHT_E 9

#define TRIG 12
#define ECHO 7

const int maxSpeed = 100; // from 0 to 100
const int distanceThreshold = 25; // an item within a range of 40 cm is considered an obstacle

void setup() {
  pinMode(IR_LEFT, INPUT);
  pinMode(IR_RIGHT, INPUT);
  
  pinMode(LEFT_F, OUTPUT);
  pinMode(LEFT_B, OUTPUT);
  pinMode(LEFT_E, OUTPUT);
  pinMode(RIGHT_F, OUTPUT);
  pinMode(RIGHT_B, OUTPUT);
  pinMode(RIGHT_E, OUTPUT);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  
  Serial.begin(9600);
  BT.begin(9600);
}

void loop() {
  if (BT.available() > 0) {
    char input = BT.read();
    if (input == 'F') {
      forwardOneUnit();
      BT.println("Done");
    } else if (input == 'R') {
      rightTurn();
      BT.println("Done");
    } else if (input == 'L') {
      leftTurn();
      BT.println("Done");
    } else if (input == 'D') { // Detect obstacle
      float distance = getDist(); 
      if (distance < distanceThreshold) {
        BT.println("Yes");
      } else {
        BT.println("No");
      }      
    }
  }
}

void forwardOneUnit() {
  // follow line
  while (digitalRead(IR_LEFT) != HIGH || digitalRead(IR_RIGHT) != HIGH) {
    if (digitalRead(IR_LEFT) == LOW && digitalRead(IR_RIGHT) == LOW) {
      forward();
    } else if (digitalRead(IR_LEFT) == LOW && digitalRead(IR_RIGHT) == HIGH) {
      axialRight();
    } else if (digitalRead(IR_LEFT) == HIGH && digitalRead(IR_RIGHT) == LOW) {
      axialLeft();
    }  
    delay(10);
  }
  stopCar();

  // drive forward a little more
  long startTime = millis();
  int duration = 1000;
  while (millis() - startTime < duration) {
    forward();
  }
  stopCar();
}

void rightTurn() {
  int lastState = digitalRead(IR_LEFT);
  int count = lastState; // left sensor needs to cross black line once, and then see it another time. 
                         // If the left sensor is already on the line, then count as first time done
  while (count < 2) {
    axialRight();
    int curState = digitalRead(IR_LEFT);
    if (curState == 1 && lastState == 0) {
      count++;
    }
    lastState = curState;
  }
  stopCar();
}

void leftTurn() {
  int lastState = digitalRead(IR_RIGHT);
  int count = lastState; // right sensor needs to cross black line once, and then see it another time. 
                         // If the right sensor is already on the line, then count as first time done
  while (count < 2) {
    axialLeft();
    int curState = digitalRead(IR_RIGHT);
    if (curState == 1 && lastState == 0) {
      count++;
    }
    lastState = curState;
  }
  stopCar();
}

float getDist() {
  long duration;
  float distance;
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  duration = pulseIn(ECHO, HIGH);
  distance = (duration / 2) * 0.03435;
  return distance;
}

void motorWrite(int a, int b, int c, int d) {
  digitalWrite(LEFT_F, a);
  digitalWrite(LEFT_B, b);
  digitalWrite(RIGHT_F, c);
  digitalWrite(RIGHT_B, d);
  analogWrite(LEFT_E, map(maxSpeed, 0, 100, 0, 255));
  analogWrite(RIGHT_E, map(maxSpeed, 0, 100, 0, 255));
}

void forward() {
  motorWrite(HIGH, LOW, HIGH, LOW);
}

void backward() {
  motorWrite(LOW, HIGH, LOW, HIGH);
}

void radialLeft() {
  motorWrite(LOW, LOW, HIGH, LOW);
}

void radialRight() {
  motorWrite(HIGH, LOW, LOW, LOW);
}

void axialLeft() {
  motorWrite(LOW, HIGH, HIGH, LOW);
}

void axialRight() {
  motorWrite(HIGH, LOW, LOW, HIGH);
}

void stopCar() {
  motorWrite(LOW, LOW, LOW, LOW);  
}
