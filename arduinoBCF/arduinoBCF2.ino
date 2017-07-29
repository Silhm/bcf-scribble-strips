

#include <SPI.h>
#include <Wire.h>
#include <stdio.h>

#include <string.h>
#include <stdlib.h>


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
static byte *lastSysEx;

static bool overload = false;


// Define the channel structure
struct channel {
  byte* trackName;
  byte displayLine1[7];
  byte displayLine2[7];
  byte offsetl1;
  byte offsetl2;
  byte* assign;
  byte* faderLevel;
  int leftPan;
  int rightPan;
};

// define all displays
static struct channel oledDisplays[7];
static int currentDisp = 0;


static int myDebug = 0;


//declare frame structure
    typedef struct {
       int start=0;
       unsigned dataSize=0;
       byte *data;
    } t_frame;


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

  byte data = MIDI.getData1();
  byte data2 = MIDI.getData2();

/*
  if (MIDI.getType() == 0xD0) { //metering?
    if (data != 0) {
      handleMetering(data);
    }
  }
  */
   if (MIDI.getType() == 0x90) { //select?
    if (data != 0 && data == 0x18) {
      currentDisp = 0;
    } 
    else if(data != 0 && data == 0x19){
      currentDisp = 1;
    }
    else if(data != 0 && data == 0x1A){
      currentDisp = 2;
    }
    refreshLCD();
   }
}



/**
   MIDI CC
*/
void HandleCC(byte channel, byte pitch, byte velocity)
{
  // Do something here with your data!
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(pitch);
  display.display();
}

/**
   MIDI note off
*/
void HandleNoteOff(byte channel, byte pitch, byte velocity)
{
  // Do something here with your data!
}

/**
   MIDI SysEx
*/
void handleSysEx(byte * sysEx, unsigned buffSize) {  
/*
  //Opening communication
  if (sysEx[5] == 0x00) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(1);
    display.println("Connection Query...");
    display.display();
    //                                        <HDR>                | Host query
    byte sysExConnectionQuery[18] = { 0xF0, 0x00, 0x00, 0x66, 0x00, 0x01, 0x36, 0x36, 0x36, 0x36, 0x36, 0x36, 0x36, 0x01, 0x01, 0x01, 0x01, 0xF7 };
    sysExConnectionQuery[4] = sysEx[4];
    MIDI.sendSysEx(18, sysExConnectionQuery, false);

    delay(500);

  }
  if (sysEx[5] == 0x02) {
    //skip protocol verifications...
    //display.clearDisplay();
    //display.setCursor(0, 0);
    display.println("Confirmed");
    display.display();
    //                                        <HDR>                | Host confirm
    byte sysExConnectionConfirm[] = { 0xf0, 0x00, 0x00, 0x66, 0x14, 0x03, 0x36, 0x36, 0x36, 0x36, 0x36, 0x36, 0x36, 0xF7 };
    MIDI.sendSysEx(14, sysExConnectionConfirm, false);
  }
*/

//* Got errors on this one
    unsigned i=0;
    int frameCpt = 0;

    t_frame frames[100];
    for(i=0; i<=buffSize;i++) {
      // Start of frame
      if(sysEx[i] == 0xF0){
        frames[frameCpt].start = i;
      }
      
      // End of frame : store it
      if(sysEx[i] == 0xF7){
        //display.print("End");
        frames[frameCpt].dataSize = 1 + i - frames[frameCpt].start ;
        memcpy(frames[frameCpt].data, sysEx + frames[frameCpt].start, frames[frameCpt].dataSize);
        frameCpt++;
      }
      
    } //end for
   
    int j=0;
    for(j=0; j<frameCpt;j++){
      if (frames[j].data[5] == 0x12) { 
        handleScribble(frames[j].data, frames[j].dataSize);
      }
    }

refreshLCD();
//end of buggy one*/

/*
  //this one is working
  //if(sysEx[0] == 0xF0){
    if (sysEx[5] == 0x12) {
      handleScribble(sysEx, buffSize);
    }
  
    refreshLCD();
  //}
  //*/
  
}


/**
   LCD message should be processed here
*/
void handleScribble(byte *sysEx, unsigned buffSize) {
  byte offset = sysEx[6];
  byte *ptr = sysEx + 7;
  // Start to get the display to update (0->7)
  int displayId = getDisplayId(sysEx);
  
    
  // Get position on the display
  if (offset >= 0x00 && offset < 0x38) {
    oledDisplays[displayId].offsetl1 = offset;
    memcpy(oledDisplays[displayId].displayLine1, ptr, 7); // get next 7 bytes (skip the 0xF7 EOSysEx)
  }
  if (offset >= 0x38 && offset <= 0x6C) { //38->6C second line
    //second line
    oledDisplays[displayId].offsetl2 = offset;
    memcpy(oledDisplays[displayId].displayLine2, ptr, 7); // get next 7 bytes (skip the 0xF7 EOSysEx)
  }

   
}

void refreshLCD(){
  //*skip display
   display.clearDisplay();
   //* Skip the Display number
  //first line (+ display number)
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.print(currentDisp + 1);
  display.setCursor(CH_WID *2, 0);
  //* Skip the first line
  display.setTextSize(2);
  //display.print(oledDisplays[currentDisp].offsetl1);
  for (int16_t i = 0; i < 7; i ++) {
    display.write(oledDisplays[currentDisp].displayLine1[i]); //write to convert Byte as char
  }
  
  //second line
  display.setTextSize(2);
  display.setCursor(0, CH_HEI * 2);
  //display.print(oledDisplays[currentDisp].offsetl2);
  display.setCursor(DP_WID_MID - (3 * CH_WID * 2), display.getCursorY()); // Center text on OLED
  for (int16_t i = 0; i < 7; i ++) {
    display.write(oledDisplays[currentDisp].displayLine2[i]); //write to convert Byte as char
  }
  //*/
  display.display();
}




void handleMetering(byte data) {
  int fullScale = DP_WID;

  byte chan = data & 0xf0; // from 0 to 7
  //TODO handle multiple displays

  byte level = data & 0x0f; // 0-> 0% , C-> 100%
  int meterVal = (level * fullScale) / 0x0C;

  display.clearDisplay();
  display.setCursor(0, 0);

  for (int16_t i = 0; i < meterVal; i += 1) {
    display.drawLine(display.getCursorX() + i, display.getCursorY(), display.getCursorX() + i, display.getCursorY() + CH_HEI, WHITE);
  }

  // Set Overload
  if (level == 0x0E) {
    overload = true;
  }
  // unset Overload
  if (level == 0x0F) {
    overload = false;
  }
  if (overload) {
    display.setTextSize(1);
    display.println(" ");
    display.print("OVERLOAD!!!!!"); //set overload
  }

  delay(50);
  display.display();
}


/**
   Get Display id
*/
int getDisplayId(byte *sysEx) {
  int offset = (sysEx[6] / 7) ; // 7char per display
  return offset % 8 ; // only 8 displays available
}









