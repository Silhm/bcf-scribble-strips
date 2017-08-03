#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>

#include <OSCBundle.h>
#include <OSCBoards.h>

#include <Wire.h>

#include "globals.h"
#include "display.h"
#include "router.h"
#include "debugData.h"


EthernetUDP Udp;
EthernetServer server(80);

byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
}; // you can find this written on the board of some Arduino Ethernets or shields

//port numbers
const unsigned int inPort = 8888;


void setup() {
  enableDebug();
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
      msgIN.route("/strip/name", stripName);
      msgIN.route("/strip/meter",stripMeter);
      msgIN.route("/strip/mute",stripMute);
      msgIN.route("/strip/solo",stripSolo);
      msgIN.route("/strip/recenable",stripRecEnable);
      msgIN.route("/strip/gain",stripGain);
      msgIN.route("/strip/pan_stereo_position",stripPan);
 
      displayStrip(1,"strip");
    }
  }
}


