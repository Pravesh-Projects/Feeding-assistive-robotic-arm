#include <MPU6050_tockn.h>
#include <Wire.h>
#include <Servo.h>
Servo myservo;
MPU6050 mpu6050(Wire);
int pos = 0;
int x=0;
long timer = 0;
int y=0;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  Wire.begin();
  myservo.write(90);
  delay(500);
  for(pos =90;pos>=40;pos-=1)
  {
    myservo.write(pos);
    delay(15);
  }
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  mpu6050.update();
  if(millis() - timer > 100)
  {
    Serial.print("gyroAngleX : ");Serial.println(mpu6050.getGyroAngleX());
    x=mpu6050.getGyroAngleX();
    if(x<-28)
    {
      y=1;
      for(pos =40;pos<=110;pos+=1)
      {
        myservo.write(pos);
        delay(35);
      }
    }
    while(y==1)
    {
      if(millis() - timer > 100)
      {
        mpu6050.update();
        Serial.println(mpu6050.getGyroAngleX());
        x=mpu6050.getGyroAngleX();
        x=map(x,-96,96,180,10);
        myservo.write(x);
        timer = millis();
      }
    }
  }
}
