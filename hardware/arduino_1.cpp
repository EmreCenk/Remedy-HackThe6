
// Tested with LCD Display, everything's working i think 

#include <LiquidCrystal.h>

LiquidCrystal lcd(2, 3, 8, 9, 10, 11);

char infoReceived;

void setup() {
  lcd.begin(16,2);
  lcd.clear();
  lcd.print("Welcome to");
  lcd.setCursor(0,1);
  lcd.print("Remedy."); 
  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0){
    infoReceived = Serial.read(); 

    if (infoReceived == 'g'){
      yesMedication();
      delay(2000);
      dispensing();
      delay(5000);
      completed();
      delay(3000);
      infoReceived = 'a';
      defaultMessage();
    }

    else if (infoReceived == 'n'){
      noMedication();
      delay(3000);
      defaultMessage();
    }

    else if (infoReceived == 'b'){
      defaultMessage();
    }
  }
}

// Action Functions

void defaultMessage(){
  lcd.clear();
  lcd.print("Welcome to");
  lcd.setCursor(0,1);
  lcd.print("Remedy.");
}

void yesMedication(){
  lcd.clear();
  lcd.print("Hi. Welcome.");
  lcd.setCursor(0,1);
  lcd.print("You Have Meds");
}

void noMedication(){
  lcd.clear();
  lcd.print("Hi. Welcome.");
  lcd.setCursor(0,1);
  lcd.print("No medication");
}

void dispensing(){
  lcd.clear();
  lcd.print("Dispensing");
  lcd.setCursor(0,1);
  lcd.print("Please Wait");
}

void completed(){
  lcd.clear();
  lcd.print("Completed");
  lcd.setCursor(0,1);
  lcd.print("Thank you!");
}