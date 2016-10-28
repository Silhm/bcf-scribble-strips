# bcf-scribble-strips
Trying to add scribble strips to BCF2000 MIDI controller via Mackie HUI protocol

This is not ready at all for now...

Wiki : https://github.com/Silhm/bcf-scribble-strips/wiki

### Features

* [TODO] Add more Scribble strips (at least 8, for the 8 channels of the BCF 2000)
* [TODO] Display track name on each display
* [TODO] Change fonts and display style
* [TODO] Add vu-meters on each channel : Metering handled, still need improvements
* [TODO] Add display for assignement and timecode/bars
* [✓] Compatible with Arduino boards UNO and MEGA (No clone or ftdi version compatibility).
* [✓] Device recognized as a MIDI device on USB connection
* [✓] Display informations on OLED screens
* [✓] Receive SysEx from Mackie HUI protocol and display accordingly
* [✓] Switch the displayed parameter as it changes (i.e : touching PAN switches to PAN view)
* [~] Handle RBG backlight on each channel (à la Behringer X-Touch)
* [~] Add Fonction keys
* [~] Add Jog Wheel
* [Future] Support OSC with ethernet shield? 


### Hardware

* Arduino UNO or MEGA flashed with HIDuino: https://github.com/ddiakopoulos/hiduino ,
* 0.96" Oled display (easy to find on ebay)
* USBTinyISP programmer


### Software

* Should be compatible out of the box without installing anything on the computer where the DAW is installed


### Development

**__Warning: this requires Arduino 1.6 or more recent versions.__**


    Work in progress... 
