#include <Servo.h>

Servo servo1;  

//void(* resetFunc) (void) = 0;


void setup() {
  servo1.attach(3);   
  Serial.begin(9600); 
  servo1.write(0);   // set one-time start position
  delay(800);       // give 0.8 second to move there
}

void loop() 
{
//  if(Serial.available()>0)  //Not needed bc it checks if the serial is connected.
//  {                         //But serial usually is connected, so should NOT use it as a trigger
                              //Bc that would constantly trigger the loop

      if(Serial.read()=='1') //Triggers if specifically '1' is received through the serial line
      {                 
                               
          servo1.write(150); // send open command...              
          delay(800);        // ... and give time to move there               
          servo1.write(0);  //send close command..             
          delay(800);   
          
       }

        // no need for an else-statement, except maybe for debugging
      
//resetFunc();

}
