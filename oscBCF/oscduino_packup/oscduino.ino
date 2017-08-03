#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>

#include <OSCBundle.h>
#include <OSCBoards.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "router.h"

// If using software SPI (the default case):
#define OLED_MOSI   4
#define OLED_CLK    5
#define OLED_DC     6
#define OLED_CS     7
#define OLED_RESET  8
Adafruit_SSD1306 display(OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, OLED_CS);

EthernetUDP Udp;
EthernetServer server(80);

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
}; // you can find this written on the board of some Arduino Ethernets or shields

//port numbers
const unsigned int inPort = 8888;

void setup() {
  // put your setup code here, to run once:
  Ethernet.begin(mac);

  display.begin(SSD1306_SWITCHCAPVCC);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("OSC informations");
  display.print("ip   : ");
  display.println(Ethernet.localIP());
  display.print("port : ");
  display.println(inPort);

  display.display();

  Serial.begin(9600);
  Serial.print("arduino is at ");
  Serial.println(Ethernet.localIP());

  Udp.begin(inPort);

}

void loop() {
OSCMsgReceive();
  
}


void OSCMsgReceive(){
  OSCMessage msgIN;
  int size;
  if((size = Udp.parsePacket())>0){
    while(size--){
      msgIN.fill(Udp.read());
    }
    if(!msgIN.hasError()){
      msgIN.route("/filter",routeTone);
      msgIN.route("/strip/name", stripName);
    }
  }
}

/*

void routeTone(OSCMessage &msg, int addrOffset ) {
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.println(msg.getInt(0));  
     display.display();
}

void stripName(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    char stripName[16];
    
    Serial.print("/strip/name ");
    Serial.print(stripId);
    Serial.print(" ");
    msg.getString(1,stripName, 16);
    Serial.print(stripName);
    Serial.println();

}
 */

