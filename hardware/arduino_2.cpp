#include <Servo.h>

Servo spinner;
Servo dispenser;

char infoReceived0;
char infoReceived1;
char infoReceived2;

void setup(){
  spinner.attach(9);
  dispenser.attach(8);

  spinner.write(0);
  dispenser.write(0); // set this to default (note to self)
  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0){
    infoReceived0 = Serial.read();

    if (infoReceived0 == 'g'){
      
      while (infoReceived0 == 'g'){
        infoReceived1 = Serial.read();

        // Depending on the barrel

        if (infoReceived1 == '0'){         
          while (infoReceived1 == '0'){
            infoReceived2 = Serial.read();
            serialChecker();
          }
          
          spinner.write(0); 
          delay(1000); 
          
          medicationDispense();
          infoReceived0 = 'a';
          infoReceived1 = '6';
          infoReceived2 = '9';
        }



        else if (infoReceived1 == '1'){         
          while (infoReceived1 == '1'){
            infoReceived2 = Serial.read();
            serialChecker();
          }
          
          spinner.write(45); 
          delay(1000); 
          
          medicationDispense();
          infoReceived0 = 'a';
          infoReceived1 = '6';
          infoReceived2 = '9';
        }




        else if (infoReceived1 == '2'){         
          while (infoReceived1 == '2'){
            infoReceived2 = Serial.read();
            serialChecker();
          }
          
          spinner.write(90); 
          delay(1000); 
          
          medicationDispense();
          infoReceived0 = 'a';
          infoReceived1 = '6';
          infoReceived2 = '9';
        }



        else if (infoReceived1 == '3'){         
          while (infoReceived1 == '3'){
            infoReceived2 = Serial.read();
            serialChecker();
          }
          
          spinner.write(145); 
          delay(1000); 
          
          medicationDispense();
          infoReceived0 = 'a';
          infoReceived1 = '6';
          infoReceived2 = '9';
        }



        else if (infoReceived1 == '4'){         
          while (infoReceived1 == '4'){
            infoReceived2 = Serial.read();
            serialChecker();
          }
          
          spinner.write(190); 
          delay(1000); 
          
          medicationDispense();
          infoReceived0 = 'a';
          infoReceived1 = '6';
          infoReceived2 = '9';
        }
      }
    }  
  }
}

// Functions

void medicationDispense(){
  delay(2000);
  int finalAmount = infoReceived2-'0';
  for (int i=finalAmount; i>0; i--){ // this for loop dispenses the pills based on how many
    dispenser.write(30);
    delay(1000);
    dispenser.write(0);
    delay(1000);
  }
}

void serialChecker(){
  if (infoReceived2 == '1'){
    infoReceived1 = '6';
  }
  else if (infoReceived2 == '2'){
    infoReceived1 = '6';
  }
  else if (infoReceived2 == '3'){
    infoReceived1 = '6';
  }
  else if (infoReceived2 == '4'){
    infoReceived1 = '6';
  }
  else if (infoReceived2 == '5'){
    infoReceived1 = '6';
  }
  else if (infoReceived2 == '6'){
    infoReceived1 = '6';
  }
}