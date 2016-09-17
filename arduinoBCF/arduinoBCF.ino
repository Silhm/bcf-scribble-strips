#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET 4


#include <MIDI.h>

MIDI_CREATE_DEFAULT_INSTANCE();

Adafruit_SSD1306 display(OLED_RESET);


#define LOGO16_GLCD_HEIGHT 16 
#define LOGO16_GLCD_WIDTH  16 

// character dimensions (for aligning text)
#define CH_WID 6
#define CH_HEI 8
// display dimensions (for aligning text)
#define DP_WID 128
#define DP_HEI 32
#define DP_WID_MID 64
#define DP_HEI_MID 16


static const unsigned char PROGMEM logo16_glcd_bmp[] =
{ B00000000, B11000000,
  B00000001, B11000000,
  B00000001, B11000000,
  B00000011, B11100000,
  B11110011, B11100000,
  B11111110, B11111000,
  B01111110, B11111111,
  B00110011, B10011111,
  B00011111, B11111100,
  B00001101, B01110000,
  B00011011, B10100000,
  B00111111, B11100000,
  B00111111, B11110000,
  B01111100, B11110000,
  B01110000, B01110000,
  B00000000, B00110000 };

#if (SSD1306_LCDHEIGHT != 32)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif



void setup() {

  MIDI.begin(MIDI_CHANNEL_OMNI);
  
  // As of the MIDI Library v3.1, the lib uses C style function 
  // pointers to create a callback system for handling input events. 
  //MIDI.setHandleNoteOn(HandleNoteOn); 
  MIDI.setHandleControlChange(HandleCC);
  //MIDI.setHandleNoteOff(HandleNoteOff);


  
  // put your setup code here, to run once:
  Serial.begin(9600);

  // by default, we'll generate the high voltage from the 3.3v line internally! (neat!)
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)
  // init done
  
  // Show image buffer on the display hardware.
  // Since the buffer is intialized with an Adafruit splashscreen
  // internally, this will display the splashscreen.
  display.display();
  delay(1);

   // Clear the buffer.
   display.clearDisplay();

//line1
  display.setTextColor(WHITE);
  displayMainText("Kick");
  
//line2
  //display.setCursor(0,10);
  
  //displayParameter("volume","42dB");
    display.setTextSize(1);

   display.clearDisplay();

   display.setCursor(0,0);
   display.print("note On  :");
   display.setCursor(0,CH_HEI);
   display.print("note Off :");
   display.setCursor(0,CH_HEI*2);
   display.print("CC       :");





    
  display.display();
  delay(1);
}

void loop() {
  // put your main code here, to run repeatedly:
  MIDI.read();
   
  /*
    display.clearDisplay();
     displayMainText("Kick");
     displayParameter("volume","");
     
  for(int16_t i=0; i<100; i+=1) {
     display.drawLine(display.getCursorX()+i, display.getCursorY(), display.getCursorX()+i, display.getCursorY()+CH_HEI, WHITE);
     display.display();
     delay(1);
  }

*/
}


//Display Kick / Snare / bass etc
void displayMainText(const char * text){
   display.setCursor(0,0);
   display.setTextSize(3);
   centerText(text);
}

void centerText(const char * text){
  display.setCursor(DP_WID_MID - (3 * CH_WID * 2),display.getCursorY());
  display.println(text);
}

void displayParameter(const char * param,const char * value){
  //display.setCursor(DP_WID_MID - (3 * CH_WID * 2),display.getCursorY());
  display.setTextSize(1);
  display.print(param);
  display.print(": ");
  display.print(value);
}


/*
void HandleNoteOn(byte channel, byte pitch, byte velocity) 
{ 
  // Do something here with your data!
   display.setCursor(7 * CH_WID ,0);
   display.print("      ");
   display.setCursor(7 * CH_WID ,0);
   display.print(pitch);
   //display.display();
   
}

void HandleNoteOff(byte channel, byte pitch, byte velocity) 
{
  // Do something here with your data!
   display.setCursor(7 * CH_WID ,CH_HEI);
   display.print("      ");
   display.setCursor(7 * CH_WID ,CH_HEI);
   display.print(pitch);
   //display.display();

}*/

void HandleCC(byte channel, byte pitch, byte velocity) 
{
  // Do something here with your data!
   display.clearDisplay();
   display.setCursor(0,0);
   display.setTextSize(3);
   display.println(pitch);
   display.setTextSize(1);
   display.println(velocity);
   display.display();

   
}

