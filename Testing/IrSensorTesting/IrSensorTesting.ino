#define LEFT_F 4
#define LEFT_B 5
#define RIGHT_F 6
#define RIGHT_B 8

#define LEFT_IR 2
#define RIGHT_IR 13

int maxSpeed = 25; // from 0 to 100

void setup() {
  pinMode(LEFT_F, OUTPUT);
  pinMode(LEFT_B, OUTPUT);
  pinMode(RIGHT_F, OUTPUT);
  pinMode(RIGHT_B, OUTPUT);

  pinMode(LEFT_IR, INPUT);
  pinMode(RIGHT_IR, INPUT);
  Serial.begin(9600);
}

bool leftDone = false;
bool rightDone = false;

void loop() {
//  int left = digitalRead(LEFT_IR);
////  int right = digitalRead(RIGHT_IR);
//  Serial.println(left);
////  Serial.print(" ");
////  Serial.println(right);
//  delay(1000);

  /*
  if (leftDone && rightDone) {
    stopCar();
  } else if (leftDone && !rightDone) {
    if (right == LOW) {
      radialLeft();
    } else {
      rightDone = true;
      stopCar();
    }
  } else if (!leftDone && rightDone) {
    if (left == LOW) {
      radialRight();
    } else {
      leftDone = true;
      stopCar();
    }
  } else {
    if (left == HIGH and right == HIGH) {
      stopCar();
      leftDone = true;
      rightDone = true;
    } else if (left == HIGH and right == LOW) {
      radialLeft();
      leftDone = true;
    } else if (left == LOW and right == HIGH) {
      radialRight();
      rightDone = true;
    } else {
      forward();
    }    
  }
  */
}

void motorWrite(int a, int b, int c, int d) {
  a = map(a, 0, 100, 0, 255);
  b = map(b, 0, 100, 0, 255);
  c = map(c, 0, 100, 0, 255);
  d = map(d, 0, 100, 0, 255);
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
