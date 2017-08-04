
EthernetUDP Udp;
EthernetServer server(80);

const char* dawURL = "asgard.strasbourg.4js.com";
const int dawPort = 3819;

void OSCConfig() {
  OSCMessage feedbackMsg("/set_surface/feedback");
  OSCMessage striplistMsg("/strip/list");
  
  feedbackMsg.add("3943");
  //feedbackMsg.add("4087");

  Udp.beginPacket(dawURL, dawPort);
  feedbackMsg.send(Udp); // send the bytes to the SLIP stream
  Udp.endPacket(); // mark the end of the OSC Packet
  feedbackMsg.empty(); // free space occupied by message

/*
  Udp.beginPacket(dawURL, dawPort);
  striplistMsg.send(Udp); // send the bytes to the SLIP stream
  Udp.endPacket(); // mark the end of the OSC Packet
  striplistMsg.empty(); // free space occupied by message
  */
}

//Start transport play
void transport_play(){
  OSCMessage startMsg("/transport_play");
  Udp.beginPacket(dawURL, dawPort);
  startMsg.send(Udp); // send the bytes to the SLIP stream
  Udp.endPacket(); // mark the end of the OSC Packet
  startMsg.empty(); // free space occupied by message
}


