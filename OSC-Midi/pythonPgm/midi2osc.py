"""
This program handle MIDI in  to OSC
"""
import argparse
import random
import time
import json

import sqlite3

import mido
from pythonosc import osc_message_builder
from pythonosc import udp_client

from lib.midiHelper import *

# Edit this to load right conf file
DAW_NAME = "ardour"


class MidiToOSC:

    def __init__(self, ipAddr, port ):

        # Init OSC client
        self._oscClient = udp_client.UDPClient(ipAddr, port)

        # Init Midi client and display available devices
        midiPort = mido.get_input_names()[0]
        self.midiIN = mido.open_input(midiPort)

        # Get the DAW OSC configuration
        with open('config/daw-osc/'+DAW_NAME+'.json', 'r') as f:
            self._dawConfig = json.load(f)



    def sendOSCMessage(self, address, values):
        """
        Send the corresponding OSC message
            - address is a string
            - value is an array
        """
        msg = osc_message_builder.OscMessageBuilder(address = address)
        
        for arg in values:
            msg.add_arg(arg)

        print(" > > OSC: "+ address + " " + str(values))
        self._oscClient.send(msg.build())



    def routeMessage(self, midiMessage):
        """
        Route midi message to the correct OSC address
        """
        print(" > route message: "+midiMessage.type)
        
        faderNotes = ["G#", "A", "A#", "B", "C", "C#", "D", "D#"]
        knobNotes = ["G#", "A", "A#", "B", "C", "C#", "D", "D#"]
        buttonNotes = ["E", "F", "F#", "G", "G#", "A", "A#", "B"]

        buttonMode = "solomute"


        # NOTE ON
        if midiMessage.type == "note_on" or  midiMessage.type == "note_off":
            midiNote = midiNumberToNote(midiMessage.note)
            note = midiNote[0]
            octave = midiNote[1]

            noteOn = midiMessage.type == "note_on"

            # Octave 7 is the fader touched
            if(octave == 7 and note in faderNotes):
                faderId = faderNotes.index(note)
                print("Fader "+ str(faderId+1)+" touched!")

            # Buttons first line
            if(octave == 0 and note in buttonNotes):
                buttonId = buttonNotes.index(note)
                self._handleButtons(1,buttonId,noteOn)

            # Buttons second line
            if(octave == 1 and note in buttonNotes):
                buttonId = buttonNotes.index(note)
                self._handleButtons(2,buttonId,noteOn)
 
            # Knob click
            """ Not yet
            if(octave == 1 and note in knobNotes):
                knobId = knobNotes.index(note)
                print("Knob : "+ str(buttonId+1)+" clicked "+str(noteOn))
            """

            # Other Buttons
            if(octave == 2):
                if(note == "G"):
                    print("Learn button clicked "+str(noteOn))
                if(note == "G#"):
                    print("Store button clicked "+str(noteOn))
                if(note == "F"):
                    print("Exit button clicked "+str(noteOn))
                if(note == "F#"):
                    print("Edit button clicked "+str(noteOn))

                # Preset / Bank 
                if(note == "A#"):
                    print("Preset < clicked "+ str(noteOn))
                if(note == "B"):
                    print("Preset > clicked "+ str(noteOn))
    
            # Four buttons in bottom of the BCF 
            if octave == 6 :
                if(note == "G"):
                    print("-Top Left- button clicked "+ str(noteOn))
                if(note == "A"):
                    print("-Top Right- button clicked "+ str(noteOn))
                if(note == "G#"):
                    print("-Bottom Left- button clicked "+str(noteOn))
                if(note == "A#"):
                    print("-Bottom Right button clicked "+str(noteOn))
        

        #pitchwheel
        if midiMessage.type == "pitchwheel" :
            faderId = midiMessage.channel
            faderValue = midiMessage.value
            
            """ 
            oscZone = "strip"
            oscType = "fader"
        
            address = self._dawConfig[oscZone][oscType]
            values = ["aaaa"]

            self.sendOSCMessage(address, values)
            """


    def read(self):
        """ Read Midi message """
        print("read midi input...")

        msg = self.midiIN.receive()
        self.routeMessage(msg)


    def _handleButtons(self, line, bId, noteOn):
        print("Button line "+ str(line) +" : "+ str(bId+1)+" clicked "+str(noteOn))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()


    midiOSC = MidiToOSC(args.ip, args.port)

    # Read Midi
    midiOSC.read()


