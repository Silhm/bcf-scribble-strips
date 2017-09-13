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


TODO
====

    - Handle rotation of Vpot
    - Be able to change button mode and vPot mode from the controller (using one of the 4 buttons on topRight?)
    - Save state of the controller (in database? in memory?)
    - Create a setup procedure 
    - Handle external displays (to display multiple things, including network setup on startup)
    - Handle external vu-meters
    - Handle webInterface for:
    - - Setup
    - - Display strips
    - - Display selected strip infos (like presonus fat channel)


IT WORKS
========

    - Sending OSC messages according to controller changes
    - Updating controller state according to OSC Messages
    - Using mapping json files to support most DAW and Controllers
