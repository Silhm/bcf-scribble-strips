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
        with open('mappings/daw-osc/'+DAW_NAME+'.json', 'r') as f:
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
        #print(" > route message: "+midiMessage.type)
        
        faderNotes = ["G#", "A", "A#", "B", "C", "C#", "D", "D#"]
        knobNotes = ["G#", "A", "A#", "B", "C", "C#", "D", "D#"]
        buttonNotes = ["E", "F", "F#", "G", "G#", "A", "A#", "B"]
        buttonNotesl2 = ["C", "C#", "D", "D#", "E", "F", "F#", "G"]

        buttonMode = "solomute"


        # NOTE ON
        if midiMessage.type == "note_on" or  midiMessage.type == "note_off":
            midiNote = midiNumberToNote(midiMessage.note)
            note = midiNote[0]
            octave = midiNote[1]

            noteOn = midiMessage.type == "note_on" and midiMessage.velocity == 127

            # Octave 7 is the fader touched
            if(octave == 7 and note in faderNotes):
                faderId = faderNotes.index(note)
                print("Fader "+ str(faderId+1)+" touched!")

            # Buttons first and second line
            if(octave == 0 and note in buttonNotes):
                buttonId = buttonNotes.index(note) 
                # octave 0 -> line 1
                self._handleButtons(1,buttonId,noteOn)
            if(octave == 1 and note in buttonNotesl2):
                buttonId = buttonNotesl2.index(note) 
                # octave 1 -> line 2
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
                    self._handleFunctionButtons("Learn", noteOn)
                if(note == "G#"):
                    self._handleFunctionButtons("Store", noteOn)
                if(note == "F"):
                    self._handleFunctionButtons("Exit", noteOn)
                if(note == "F#"):
                    self._handleFunctionButtons("Edit", noteOn)

                # Preset / Bank 
                if(note == "A#"):
                    self._handleBankButtons("<", noteOn)
                if(note == "B"):
                    self._handleBankButtons(">", noteOn)
    
            # Four buttons in bottom of the BCF 
            if octave == 6 :
                if(note == "G"):
                    self._handleFunctionButtons("TopLeft", noteOn)
                if(note == "G#"):
                    self._handleFunctionButtons("TopRight", noteOn)
                if(note == "A"):
                    self._handleFunctionButtons("BottomLeft", noteOn)
                if(note == "A#"):
                    self._handleFunctionButtons("BottomRight", noteOn)

        #pitchwheel
        if midiMessage.type == "pitchwheel" :
            self._handlePitchWheel(midiMessage.channel, midiMessage.pitch)
            
            """ 
            oscZone = "strip"
            oscType = "fader"
        
            address = self._dawConfig[oscZone][oscType]
            values = ["aaaa"]

            self.sendOSCMessage(address, values)
            """


    def read(self):
        """ Read Midi message """

        msg = self.midiIN.receive()
        self.routeMessage(msg)

        self.read()


    def _handleButtons(self, line, bId, noteOn):
        print("Button line "+ str(line) +" : "+ str(bId+1)+" clicked "+str(noteOn))

    def _handleFunctionButtons(self, name, clicked):
        print("F Button " + str(name) +" "+str(clicked))

    def _handleBankButtons(self, name, clicked):
        print("Bank" + str(name) +" "+str(clicked))


    def _handlePitchWheel(self, ch, value):
        faderId = ch
        faderValue = value
        print("Fader "+str(ch+1)+" position "+str(value))





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()


    midiOSC = MidiToOSC(args.ip, args.port)

    # Read Midi
    print("read midi input...")
    midiOSC.read()


