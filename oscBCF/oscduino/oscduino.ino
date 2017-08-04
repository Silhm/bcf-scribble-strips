#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>

#include <OSCBundle.h>
#include <OSCBoards.h>

#include <Wire.h>

#include "globals.h"
#include "display.h"
#include "router.h"
#include "osc.h"
#include "debugData.h"




byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
}; // you can find this written on the board of some Arduino Ethernets or shields

//port numbers
const unsigned int inPort = 8888;


void setup() {
  //enableDebug();

  Ethernet.begin(mac);

  display.begin(SSD1306_SWITCHCAPVCC);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println(" Informations ");
  display.print("ip   : ");
  display.println(Ethernet.localIP());
  display.print("port : ");
  display.println(inPort);
  display.display();

  Serial.begin(9600);
  //Serial.print("arduino is at ");
  //Serial.println(Ethernet.localIP());

  Udp.begin(inPort);

  OSCConfig();
}

void loop() {
  OSCMsgReceive();
}


void OSCMsgReceive(){
  OSCMessage msgIN;
  int size;
  char toto[28];
  if((size = Udp.parsePacket())>0){
    while(size--){
      msgIN.fill(Udp.read());
    }
    if(!msgIN.hasError()){

     /* DEBUGGER
      //if(msgIN.getType(0) == 's'){
         Serial.println(msgIN.bytes());
         msgIN.getString(0, toto, 20 );
         Serial.println(toto);
         msgIN.getAddress(buff,0);
         Serial.println(buff);
    
      //}
      //*/
      
      msgIN.route("/select/name", stripName);
      msgIN.route("/select/mute",stripMute);
      msgIN.route("/select/solo",stripSolo);
      msgIN.route("/select/recenable",stripRecEnable);

      msgIN.route("/strip/meter",stripMeter);
      
      /*
      msgIN.route("/strip/meter",stripMeter);
      msgIN.route("/strip/mute",stripMute);
      msgIN.route("/strip/solo",stripSolo);
      msgIN.route("/strip/recenable",stripRecEnable);
      msgIN.route("/strip/gain",stripGain);
      msgIN.route("/strip/pan_stereo_position",stripPan);
 */
      displayStrip(1,"strip");
    }
  }
}


