#define LEFT_F 3
#define LEFT_B 5
#define RIGHT_F 6
#define RIGHT_B 9

#define BUTTON_PIN 7

int maxSpeed = 50; // from 0 to 100

int gridLength = 30; // in centimeters
int delayAfterMove = 1000; // in milliseconds

int forwardTime = 735;
int rightTurnTime = 260;
int leftTurnTime = 260;

float rightWeight = 0.9;
float leftWeight = 1;

void setup() {
  Serial.begin(9600);
  pinMode(LEFT_F, OUTPUT);
  pinMode(LEFT_B, OUTPUT);
  pinMode(RIGHT_F, OUTPUT);
  pinMode(RIGHT_B, OUTPUT);

  pinMode(BUTTON_PIN, INPUT);

  /*
  Serial.begin(9600);
  delay(2000);
  String directions = "F";
//  "FRFLFRFRFRFLFRFR";
  for (int i = 0; i < directions.length(); i++) {
    if (directions[i] == 'F') {
      forwardOneGrid();
    } else if (directions[i] == 'R') {
      right90Deg();
    } else if (directions[i] == 'L') {
      left90Deg();
    }
  }
  */
}

void loop() {
  int state = digitalRead(BUTTON_PIN);
  if (state == HIGH) {
    delay(2000);
    String directions = "FFF";
    for (int i = 0; i < directions.length(); i++) {
      if (directions[i] == 'F') {
        forwardOneGrid();
      } else if (directions[i] == 'R') {
        right90Deg();
      } else if (directions[i] == 'L') {
        left90Deg();
      }  
    }
  }
}

void forwardOneGrid() {
  forward();
  delay(forwardTime);
  stopCar();
  delay(delayAfterMove);
}

void right90Deg() {
  axialRight();
  delay(rightTurnTime);
  stopCar();
  delay(delayAfterMove);
}

void left90Deg() {
  axialLeft();
  delay(leftTurnTime);
  stopCar();
  delay(delayAfterMove);
}

void motorWrite(int a, int b, int c, int d) {
  a = map(a, 0, 100, 0, 255) * leftWeight;
  b = map(b, 0, 100, 0, 255) * leftWeight;
  c = map(c, 0, 100, 0, 255) * rightWeight;
  d = map(d, 0, 100, 0, 255) * rightWeight;
  analogWrite(LEFT_F, a);
  analogWrite(LEFT_B, b);
  analogWrite(RIGHT_F, c);
  analogWrite(RIGHT_B, d);
}

void forward() {
  motorWrite(maxSpeed, 0, maxSpeed, 0);
}

void backward() {
  motorWrite(0, maxSpeed, 0, maxSpeed);
}

void radialLeft() {
  motorWrite(0, 0, maxSpeed, 0);
}

void radialRight() {
  motorWrite(maxSpeed, 0, 0, 0);
}

void axialLeft() {
  motorWrite(0, maxSpeed, maxSpeed, 0);
}

void axialRight() {
  motorWrite(maxSpeed, 0, 0, maxSpeed);
}

void stopCar() {
  motorWrite(0, 0, 0, 0);  
}
