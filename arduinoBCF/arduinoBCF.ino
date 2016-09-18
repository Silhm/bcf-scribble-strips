#include <SPI.h>
#include <Wire.h>

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <MIDI.h>

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

  MIDI.begin(MIDI_CHANNEL_OMNI);

  // MIDI callback system for handling input events.
  //MIDI.setHandleNoteOn(HandleNoteOn);
  //MIDI.setHandleControlChange(HandleCC);
  //MIDI.setHandleNoteOff(HandleNoteOff);
  //MIDI.setHandleSystemExclusive(HandleSysEx);

  Serial.begin(9600);

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

const byte * toto;


enum MidiType{
  InvalidType           = 0x00,    
  NoteOff               = 0x80,    
  NoteOn                = 0x90,    
  AfterTouchPoly        = 0xA0,    
  ControlChange         = 0xB0,    
  ProgramChange         = 0xC0,    
  AfterTouchChannel     = 0xD0,    
  PitchBend             = 0xE0,    
  SystemExclusive       = 0xF0,    
  TimeCodeQuarterFrame  = 0xF1,   // 241 
  SongPosition          = 0xF2,    
  SongSelect            = 0xF3,    
  TuneRequest           = 0xF6,    
  Clock                 = 0xF8,    
  Start                 = 0xFA,    
  Continue              = 0xFB,    
  Stop                  = 0xFC,    
  ActiveSensing         = 0xFE,    
  SystemReset           = 0xFF,    
};


/**
   MAIN loop, mostly reading MIDI messages
*/
void loop() {



  //PING Mackie HUI protocol on DAW
  // note on, key 0, velocity 0
  //MIDI.sendNoteOn(0,0,1);

  
  // Reading MIDI messages, // not handling them via Callback
  MIDI.read();
  display.clearDisplay();
  display.setCursor(0, 0);
  display.display();
  switch (MIDI.getType()) {
    case 0xB0:
      display.print("CC");
     break;
    case 0xF0:
      display.setCursor(0, CH_HEI*2); //display IT on 3rd line
      display.print("SysEx");
     break;
    case 0x80:
      display.print("NoteOff");
     break;
    case 0x90:
      display.print("NoteOn");
     break;
    case 0xFE:
      display.print("ActiveSensing");
     break;
    case 0xC0:
      display.print("PC");
     break;
    case 0xA0:
      display.print("AfterTouchPoly");
     break;
    case 0xD0:
      display.print("AfterTouchChannel");
     break;
    case 0xFC:
      display.print("Stop");
     break;
    case 0xFF:
      display.print("SystemReset");
     break;
    case 0xE0:
      display.print("PitchBend");
     break;
    default:
      display.setCursor(0, CH_HEI);
      display.print(MIDI.getType());
      break;
  }
  
  display.display();
  //display.print(MIDI.getSysExArrayLength());


   /*
  for (int16_t i = 0; i < MIDI.getSysExArrayLength(); i += 1) {
    display.print(toto[i]);
  }
  */
  display.display();
  
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
  display.print(channel);
  display.print(":");
  display.print(pitch);
  display.print(":");
  display.println(velocity);
  display.display();

  /*
     if(channel == 0xa0){
        display.clearDisplay();
        display.setCursor(0,0);
        display.setTextSize(3);
        display.println("woot");

        display.setTextSize(1);
        if(pitch == 0){
             display.print("L :");
             display.print(velocity);
        }
        else{
             display.print("R : ");
             display.print(velocity);

        }


        display.display();
     }
  */
}


/**
   MIDI SysEx
*/
void HandleSysEx(byte *array, unsigned size) {

  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("SysEx");
  display.print(array[0]);
  display.display();


}










