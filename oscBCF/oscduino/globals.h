#define H_GLOBALS

// Define the channel structure
struct strip {
  int ssid;
  char trackName[16];
  float faderPos;
  float instantSignal;
  float panPos;
  bool recEnable;
  bool solo;
  bool mute;
  float gain;
  bool selected;
};

struct transport {
  bool stopState;
  bool playState;
  bool loopToggleState;
  bool recToggleState;
};

strip Gstrip;


