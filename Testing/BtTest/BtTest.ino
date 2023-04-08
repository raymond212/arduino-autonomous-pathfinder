#include <SoftwareSerial.h>
SoftwareSerial BT(10, 11);

#define LED 13

void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  pinMode(LED, OUTPUT);
}

int state = 0;



void loop() {
  // Normal serial
//  if (Serial.available()) {
//    char input = Serial.read();
//    if (input == '0') {
//      digitalWrite(LED, LOW);
//      Serial.println("OFF");
//    } else if (input == '1') {
//      digitalWrite(LED, HIGH);
//      Serial.println("ON");
//    }
//  }

  // Bluetooth serial
  if (BT.available() > 0) {
    char input = BT.read();
    if (input == '0') {
      digitalWrite(LED, LOW);
      BT.println("OFF");
    } else {
//    } else if (input == '1') {
      digitalWrite(LED, HIGH);
      BT.println("ON");
    }
  }
}
