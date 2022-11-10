// Sketch for driving in different directions
// Input for directions through serial
// Forward, Backward, Left turn, Right turn

//For communicating with the mBot arduino board
#include "MeMCore.h"

//Initialize the Matrix board
MeLEDMatrix ledMtx_1(1);
unsigned char drawBuffer[16];
unsigned char *drawTemp;

// initializing the motors
MeDCMotor motor1(M1);
MeDCMotor motor2(M2);

//initialize speed
int leftspeed = 0; /* value: between -255 and 255. */
int rightspeed = 0; /* value: between -255 and 255. */
int speed = 100;

// the onboard LED
byte ledPin = 13;

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

  //Draw the Fish on the Matrix board
  ledMtx_1.setColorIndex(1);
  ledMtx_1.setBrightness(6);
  drawTemp = new unsigned char[16] {255, 129, 66, 36, 24, 24, 36, 66, 129, 129, 129, 129, 137, 66, 36, 24};
  memcpy(drawBuffer, drawTemp, 16);
  free(drawTemp);
  ledMtx_1.drawBitmap(0, 0, 16, drawBuffer);
}

void loop()
{
  if (Serial.available()) {
    char command = Serial.read(); //command should be a char
    if (command == 'w') { //forward
      leftspeed = speed;
      rightspeed = speed;
      digitalWrite(ledPin, ! digitalRead(ledPin)); // change the state of the LED everytime a command is executed
//      Serial.println(command); // printing the given command. Can be used for debugging
//      Serial.println("Driving Forward");
    }
    else if (command == 'a') { //left
      leftspeed = 0;
      rightspeed = speed;
      digitalWrite(ledPin, ! digitalRead(ledPin));
//      Serial.println(command);
//      Serial.println("Turning Left");
    }
    else if (command == 's') { //backward
      leftspeed = -speed;
      rightspeed = -speed;
      digitalWrite(ledPin, ! digitalRead(ledPin));
//      Serial.println(command);
//      Serial.println("Driving Backward");
    }
    else if (command == 'd') { //right
      leftspeed = speed;
      rightspeed = 0;
      digitalWrite(ledPin, ! digitalRead(ledPin));
//      Serial.println(command);
//      Serial.println("Turning Right");
    }
    else if (command == 'q') { //Stop
      leftspeed = 0;
      rightspeed = 0;
      digitalWrite(ledPin, ! digitalRead(ledPin));
//      Serial.println(command);
//      Serial.println("Stopping");
    }
  }
  //  else {
  //    Serial.println("Invalid command");
  //    Serial.println(leftspeed);
  //    Serial.println(rightspeed);
  //  }
  motor1.run((M1) == M1 ? -(leftspeed) : (leftspeed));
  motor2.run((M2) == M1 ? -(rightspeed) : (rightspeed));
}
