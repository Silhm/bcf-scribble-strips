#ifndef H_DISPLAY
#include "display.h"
#endif
#ifndef H_GLOBALS
#include "globals.h"
#endif
    
void stripMeter(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    char meter[16];
    msg.getString(1,meter, 16);
    strcpy (Gstrip.trackName,meter);
}

void stripMute(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    Gstrip.mute = msg.getInt(1);
    Serial.print("mute ");
    Serial.println(Gstrip.mute);
}

void stripSolo(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    Gstrip.solo = msg.getInt(1);
}

void stripRecEnable(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    Gstrip.recEnable = msg.getInt(1);
}

void stripGain(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    Gstrip.gain = msg.getFloat(1);
}

void stripPan(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    Gstrip.panPos = msg.getFloat(1);
}





void stripName(OSCMessage &msg, int addrOffset ){
    int stripId = msg.getInt(0);
    char stripName[16];
    msg.getString(1,stripName, 16);
  
    Gstrip.ssid = stripId;
    strcpy (Gstrip.trackName,stripName);
       
    Serial.print("/strip/name ");
    Serial.print(stripId);
    Serial.print(" ");
  
    Serial.print(stripName);
    Serial.println();

}



