#include <Servo.h>

Servo myservo;
int incomingByte = 0;
void setup() {
  Serial.begin(9600);  
  myservo.attach(3); 
  myservo.write(90); 
  Serial.println("Servo ok");
}

void loop() {

  if (Serial.available() > 0) {
    incomingByte = Serial.read(); 
    Serial.print("Received: ");
    Serial.println((char)incomingByte);

    switch (incomingByte) {
      case '0': 
        Serial.println("Servo at 90°");
        myservo.write(90);
        break;

      case '1':
        Serial.println("Servo at 180°");
        myservo.write(180);
        delay(500);
        myservo.write(90);
        break;

      case '2':
        Serial.println("Servo at 0°");
        myservo.write(0);
        delay(500); 
        myservo.write(90);
        break;

      default: 
        Serial.println("unknown");
        myservo.write(90);
        break;
    }
  }
}

