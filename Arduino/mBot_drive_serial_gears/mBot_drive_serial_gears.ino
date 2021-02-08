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

//initialize speed and gears
int leftspeed = 0; /* value: between -255 and 255. */
int rightspeed = 0; /* value: between -255 and 255. */
int speed = 100;
int gear = 0; /* gear value 0,1,2 */
int gearspeed[] = {100, 175, 250};

// the onboard LED
byte ledPin = 13;

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

  //Draw a Fish on the Matrix board
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
    else if (command == 'e') { //360 left
      leftspeed = -speed;
      rightspeed = speed;
      digitalWrite(ledPin, ! digitalRead(ledPin));
      //      Serial.println(command);
      //      Serial.println("360 Left");
    }
    else if (command == 'r') { //360 right
      leftspeed = speed;
      rightspeed = -speed;
      digitalWrite(ledPin, ! digitalRead(ledPin));
      //      Serial.println(command);
      //      Serial.println("360 right");
    }
    else if (command == 'p' && gear < 2) { //gear up
      gear += 1;
      speed = gearspeed[gear]; // update speed variable
      
      // update driving speed immediatly when gear is changed
      if (leftspeed > 0 && rightspeed > 0) { //forward
        leftspeed = gearspeed[gear];
        rightspeed = gearspeed[gear];
      }
      if (leftspeed < 0 && rightspeed < 0) { //backward
        leftspeed = -gearspeed[gear];
        rightspeed = -gearspeed[gear];
      }
      if (rightspeed > 0 && leftspeed == 0) { //left turn
        rightspeed = gearspeed[gear];
      }
      if (leftspeed > 0 && rightspeed == 0) { // right turn
        leftspeed = gearspeed[gear];
      }
      if (leftspeed < 0 && rightspeed > 0) { //360 left
        leftspeed = -gearspeed[gear];
        rightspeed = gearspeed[gear];
      }
      if (leftspeed > 0 && rightspeed < 0) { //360 right
        leftspeed = gearspeed[gear];
        rightspeed = -gearspeed[gear];
      }
      digitalWrite(ledPin, ! digitalRead(ledPin));
      //      Serial.println(command);
      //      Serial.println(gear);
      //      Serial.println("Gear up");
    }
    else if (command == 'o' && gear > 0) { //gear down
      gear -= 1;
      speed = gearspeed[gear]; // update speed variable

      // update driving speed immediatly when gear is changed
      if (leftspeed > 0 && rightspeed > 0) { //forward
        leftspeed = gearspeed[gear];
        rightspeed = gearspeed[gear];
      }
      if (leftspeed < 0 && rightspeed < 0) { //backward
        leftspeed = -gearspeed[gear];
        rightspeed = -gearspeed[gear];
      }
      if (rightspeed > 0 && leftspeed == 0) { //left turn
        rightspeed = gearspeed[gear];
      }
      if (leftspeed > 0 && rightspeed == 0) { // right turn
        leftspeed = gearspeed[gear];
      }
      if (leftspeed < 0 && rightspeed > 0) { //360 left
        leftspeed = -gearspeed[gear];
        rightspeed = gearspeed[gear];
      }
      if (leftspeed > 0 && rightspeed < 0) { //360 right
        leftspeed = gearspeed[gear];
        rightspeed = -gearspeed[gear];
      }
      digitalWrite(ledPin, ! digitalRead(ledPin));
      //      Serial.println(command);
      //      Serial.println(gear);
      //      Serial.println("Gear down");
    }
    else if (command == 'q') { //stopping
      leftspeed = 0;
      rightspeed = 0;
      digitalWrite(ledPin, ! digitalRead(ledPin));
      //      Serial.println(command);
      //      Serial.println("Stopping");
    }
    else if (command == 'h') { //DEBUG prints all variables of interest
      digitalWrite(ledPin, ! digitalRead(ledPin));
      Serial.print("Command: ");
      Serial.println(command);
      Serial.print("Leftspeed: ");
      Serial.println(leftspeed);
      Serial.print("Rightspeed: ");
      Serial.println(rightspeed);
      Serial.print("Gear: ");
      Serial.println(gear);
      Serial.println("Gearspeeds:");
      Serial.println(gearspeed[0]);
      Serial.println(gearspeed[1]);
      Serial.println(gearspeed[2]);
      Serial.println(gearspeed[3]);
    }
  }
  motor1.run((M1) == M1 ? -(leftspeed) : (leftspeed));
  motor2.run((M2) == M1 ? -(rightspeed) : (rightspeed));
}
