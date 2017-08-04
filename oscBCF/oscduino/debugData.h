#ifndef H_GLOBALS
#include "globals.h"
#endif

void enableDebug(){

  Gstrip.ssid = 1;
  strcpy(Gstrip.trackName, "Snare");
  Gstrip.faderPos = 1;
  Gstrip.meter = -12,9;
  Gstrip.panPos = 0.3;
  Gstrip.recEnable = false;
  Gstrip.solo = true;
  Gstrip.mute = false;
  Gstrip.gain = 0;
  Gstrip.selected = false;

  
}

