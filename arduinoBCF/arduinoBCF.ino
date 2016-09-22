

#include <SPI.h>
#include <Wire.h>
#include <stdio.h>



#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <midi_Namespace.h>
#include <MIDI.h>
#include <midi_Message.h>
#include <midi_Defs.h>
#include <midi_Settings.h>



//Oled related
#define OLED_RESET 4
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

Adafruit_SSD1306 display(OLED_RESET);

MIDI_CREATE_DEFAULT_INSTANCE();
#define   MIDI_NAMESPACE   midi

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
  B00000000, B00110000
};

#if (SSD1306_LCDHEIGHT != 32)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

//MIDI buffer
byte buffer[10];


/**
   Board Setup
*/
void setup() {

   MIDI.begin();
   MIDI.turnThruOff();
   MIDI.setHandleSystemExclusive(handleSysEx);

  // MIDI callback system for handling input events.
  //MIDI.setHandleNoteOn(HandleNoteOn);
  //MIDI.setHandleControlChange(HandleCC);
  //MIDI.setHandleNoteOff(HandleNoteOff);

  //Serial.begin(9600);

  // by default, we'll generate the high voltage from the 3.3v line internally! (neat!)
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)

  // Show image buffer on the display hardware.
  // Since the buffer is intialized with an Adafruit splashscreen
  // internally, this will display the splashscreen.
  display.display();
  delay(1);
  display.clearDisplay();

  // Loading message
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.setTextSize(2);
  display.println("BCF 2000");
  display.setTextSize(1);
  display.print("Init: ");
  for (int16_t i = 0; i < 100; i += 1) {
    display.drawLine(display.getCursorX() + i, display.getCursorY(), display.getCursorX() + i, display.getCursorY() + CH_HEI, WHITE);
    display.display();
    delay(1);
  }
  display.print("OK!");
  display.display();
  delay(100);
  display.clearDisplay();
  display.drawPixel(10, 10, WHITE);
  display.display();
}

/**
   MAIN loop, mostly reading MIDI messages
*/
void loop() {
  // Reading MIDI messages, 
  
  MIDI.read();
  

}



/**
   MIDI CC
*/
void HandleCC(byte channel, byte pitch, byte velocity)
{
  // Do something here with your data!
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("MIDI CC");
  display.display();
}


/**
   MIDI SysEx
*/
void handleSysEx(byte * sysEx, unsigned buffSize) {
  //header f0 00 00 66 05 00 
  //       
  display.clearDisplay();


  if(sysEx[5] == 0x12){
    handleScribble(sysEx, buffSize);
  }
 

  /*
  if(sysEx[5] == 0x20){
    // <hdr> 20 05 00 <eof>
    handleMetering(sysEx, buffSize);
  }
  */
  


  display.display();
}


/**
 * LCD message should be processed here
 */
void handleScribble(byte *sysEx, unsigned buffSize){
    byte offset = sysEx[6];
    // Start to get the display to update (0->7)
    int displayId = getDisplayId(sysEx);
    

    if(displayId == 0){
      // Get position on the display
      if(offset>=0 && offset <= 37){
          //first line 
          display.setTextSize(2); 
          display.setCursor(0,0);
      }
      else{ //38->6C second line
          //second line
          display.setTextSize(2);
          display.setCursor(0,CH_HEI*2);
          display.setCursor(DP_WID_MID - (3 * CH_WID * 2),display.getCursorY()); // Center text on OLED
         
      }   
  
      //Display the message 
      for (int16_t i = 7; i < buffSize-1; i ++) {
          display.write(sysEx[i]); //write to convert Byte as char
      }   
    }
}


void handleMetering(byte *sysEx, unsigned buffSize){
    //TODO
    byte offset = sysEx[6];
    // Start to get the display to update (0->7)
    int displayId = getDisplayId(sysEx);
     display.setTextSize(2); 
     display.setCursor(0,0);
    
     display.write(sysEx[7]); //write to convert Byte as char
     display.write(sysEx[8]); //write to convert Byte as char
}


/**
 * Get Display id
 */
int getDisplayId(byte *sysEx){
    int offset = (sysEx[6] / 7) ; // 7char per display
    return offset % 8 ; // only 8 displays available
}









