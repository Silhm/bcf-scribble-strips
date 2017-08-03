#define H_DISPLAY
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


// If using software SPI (the default case):
#define OLED_MOSI   4
#define OLED_CLK    5
#define OLED_DC     6
#define OLED_CS     7
#define OLED_RESET  8

Adafruit_SSD1306 display(OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, OLED_CS);


void displayPan(float panValue){
    //centered line
    float hMiddle = display.width()/2;
    float vMiddle = display.height()/2;

    // 0.5 is 0
    // 0   is -100
    // 1   is 100
    // 0.3 is ?
    
    display.drawLine(hMiddle, 20, hMiddle, 40, WHITE);
  
    /*display.setCursor(5, 20);
    
    
    //display.print(panValue); 
    Serial.print("panValue ");
    Serial.println(panValue);*/
}


/**
 * ssid to display
 */
void displayStrip(int ssid, const char* mode){
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(2, 0);
  display.print(Gstrip.ssid); 

  //Track Name
  display.setCursor(20, 0);
  display.setTextSize(2);
  display.println(Gstrip.trackName);

  if(mode == "strip"){
    display.setTextSize(1);
    //Solo
    if(Gstrip.solo){
      //x0, y0, w, h, rad, col
      display.fillRoundRect(0, 10, 11, 10, 2, WHITE);
      display.setTextColor(BLACK);
      display.setCursor(3, 10);
      display.print("s");
      display.setTextColor(WHITE);
    }
    else{
      display.drawRoundRect(0, 10, 11, 10, 2, WHITE);
      display.setTextColor(WHITE);
      display.setCursor(3, 10);
      display.print("s");
    }
  
    //Mute
    if(Gstrip.mute){
      //x0, y0, w, h, rad, col
      display.fillRoundRect(0, 22, 11, 10, 2, WHITE);
      display.setTextColor(BLACK);
      display.setCursor(3, 22);
      display.print("m");
      display.setTextColor(WHITE);
    }
    else{
      display.drawRoundRect(0, 22, 11, 10, 2, WHITE);
      display.setTextColor(WHITE);
      display.setCursor(3, 22);
      display.print("m");
  }

  }
  else if(mode == "pan"){
    displayPan(Gstrip.panPos);
  }
 
  display.display();
}




