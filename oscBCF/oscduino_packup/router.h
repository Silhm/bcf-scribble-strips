
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



