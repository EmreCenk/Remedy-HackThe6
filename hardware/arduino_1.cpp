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