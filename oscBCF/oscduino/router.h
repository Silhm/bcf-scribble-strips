#ifndef H_DISPLAY
#include "display.h"
#endif
#ifndef H_GLOBALS
#include "globals.h"
#endif
    
char buff[120];


void stripMeter(OSCMessage &msg, int addrOffset ){
    msg.getAddress(buff,0);
    char stripId = atoi (buff+addrOffset+1);
 
    Serial.print(stripId);
    Serial.print(msg.getFloat(0));
    
    if(stripId == 1){
      Gstrip.meter,msg.getFloat(0);
    }
    
}

void stripMute(OSCMessage &msg, int addrOffset ){
    if(msg.getType(0) == 'f'){
      Gstrip.mute = int(msg.getFloat(0));
    }
    else{
      Gstrip.mute = msg.getInt(0);
    }
}

void stripSolo(OSCMessage &msg, int addrOffset ){
    if(msg.getType(0) == 'f'){
      Gstrip.solo = int(msg.getFloat(0));
    }
    else{
      Gstrip.solo = msg.getInt(0);
    }
}

void stripRecEnable(OSCMessage &msg, int addrOffset ){
   if(msg.getType(0) == 'f'){
      Gstrip.recEnable = int(msg.getFloat(0));
    }
    else{
      Gstrip.recEnable = msg.getInt(0);
    }
}

void stripGain(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
     if(stripId == 1){
      Gstrip.gain = msg.getFloat(1);
     }
}

void stripPan(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
     if(stripId == 1){
      Gstrip.panPos = msg.getFloat(1);
     }
}


void stripName(OSCMessage & msg, int addrOffset ){
    msg.getAddress(buff,0);
    char stripId = atoi (buff+addrOffset+1);
    char stripName[9];

     Serial.println(stripId);

     //if(stripId == 1){
      msg.getString(0,stripName, 9);
      Gstrip.ssid = stripId;
      strncpy (Gstrip.trackName,stripName,9);
     //}
}
