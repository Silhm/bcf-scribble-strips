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
   int offsetX = 17;
   
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(2, 0);
  display.print(Gstrip.ssid); 

  //Track Name
  display.setCursor(20, 1);
  display.setTextSize(2);
  
  if(Gstrip.selected){
    display.fillRoundRect(offsetX, 0, 110, 17, 2, WHITE);
    display.setTextColor(BLACK); 
  }
  display.println(Gstrip.trackName);
  display.setTextColor(WHITE); 

  if(mode == "strip"){
    display.setTextSize(1);
    //Solo
    if(Gstrip.solo){
      //x0, y0, w, h, rad, col
      display.fillRoundRect(offsetX + 5, 20, 30, 12, 2, WHITE);
      display.setTextColor(BLACK);
      display.setCursor(offsetX + 8, 22);
      display.print("solo");
      display.setTextColor(WHITE);
    }
    else{
      display.drawRoundRect(offsetX + 5, 20, 30, 12, 2, WHITE);
      display.setTextColor(WHITE);
      display.setCursor(offsetX + 8, 22);
      display.print("solo");
    }

    //Mute
    if(Gstrip.mute){
      //x0, y0, w, h, rad, col
      display.fillRoundRect(offsetX + 45, 20, 31, 12, 2, WHITE);
      display.setTextColor(BLACK);
      display.setCursor(offsetX + 49, 22);
      display.print("mute");
      display.setTextColor(WHITE);
    }
    else{
      display.drawRoundRect(offsetX + 45, 20, 31, 12, 2, WHITE);
      display.setTextColor(WHITE);
      display.setCursor(offsetX + 49, 22);
      display.print("mute");
   }

    //Rec
    if(Gstrip.recEnable){
      //x0, y0, w, h, rad, col
      display.fillRoundRect(offsetX + 85, 20, 23, 12, 2, WHITE);
      display.fillCircle(offsetX + 96, 26, 4, BLACK);
    }
      else{
      display.drawRoundRect(offsetX + 85, 20, 23, 12, 2, WHITE);
      display.fillCircle(offsetX + 96, 26, 4, WHITE);
    }

    //Meter TODO
    // -200 to 0
    //min 1930
    // max > 0 is clipping
    //Gstrip.meter
    int height = -9 * Gstrip.meter ;
    display.fillRect(2, 10, 6, 22, WHITE);
    //fill with void
    display.fillRect(2, 10, 6, height, BLACK);

    
  
  }
  else if(mode == "pan"){
    displayPan(Gstrip.panPos);
  }
 
  display.display();
}




