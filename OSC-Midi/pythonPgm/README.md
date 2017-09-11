Work in progress...

The main purpose here is to convert MIDI message from the midi controller in LogicControl emulation mode 
into OSC messages for the DAW

Next step is to convert OSC messages from the DAW to the midi controller 

Final step is to route OSC message to Oled displays and Vu-meters


Mappings Directory contains Mappings of :

    - OSC message for each supported DAW
    - Midi message used by each supported Controllers


midi2osc.py converts midi messages from controller to DAW as OSC messages
osc2midi.py converts DAW OSC message to midi messages for the midi controller
setup.py will initialize database (not yet)
