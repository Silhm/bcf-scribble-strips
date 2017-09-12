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
from mappings.mapping import ControllerConfig, DawConfig


# Edit this to load right conf file
DAW_NAME = "ardour"
CONTROLLER_NAME = "bcf2000"
BANK_SIZE = 8 

class MidiToOSC:

    def __init__(self, ipAddr, port ):

        # Init OSC client
        print("OSC will be sent on "+ipAddr+":"+str(port)) 
        self._oscClient = udp_client.UDPClient(ipAddr, port)

        # Init Midi client and display available devices
        midiPort = mido.get_input_names()[0]
        self.midiIN = mido.open_input(midiPort)

        # Get the DAW OSC configuration
        self.dawConfig = DawConfig(DAW_NAME)

        # Get the Controller MIDI configuration
        self.ctrlConfig = ControllerConfig(CONTROLLER_NAME)

        self.buttonMode = "solomute"
        self.bank = 0


    def sendOSCMessage(self, address, values):
        """
        Send the corresponding OSC message
            - address is a string
            - value is an array
        """
        msg = osc_message_builder.OscMessageBuilder(address = address)
        
        for arg in values:
            msg.add_arg(arg)

        print(" > > OSC: {} {}".format(address,values))
        self._oscClient.send(msg.build())



    def routeMessage(self, midiMessage):
        """
        Route midi message to the correct OSC address
        """
        print(" > route message: {}".format(midiMessage))
        
        faderNotes = map(midiFullNoteToNumber, self.ctrlConfig.getFaderNotes())
        #vPotNotes = ["G#", "A", "A#", "B", "C", "C#", "D", "D#"]
        buttonNotes = self.ctrlConfig.getButtonNotes("line1")
        buttonNotesl2 = self.ctrlConfig.getButtonNotes("line2")
 

        # NOTE ON
        if midiMessage.type == "note_on" or  midiMessage.type == "note_off":
            midiNote = midiNumberToNote(midiMessage.note)
            note = midiNote[0]
            octave = midiNote[1]

            noteOn = midiMessage.type == "note_on" and midiMessage.velocity == 127

            # Octave 7 is the fader touched
            if(octave == 7 and note in faderNotes):
                faderId = faderNotes.index(note)
                print("Fader "+ str(faderId+1)+" touched! "+str(noteOn))

            # Buttons first and second line
            if(octave == 0 and note in buttonNotes):
                buttonId = buttonNotes.index(note) 
                # octave 0 -> line 1
                self._handleButtons(1,buttonId,noteOn)
            if(octave == 1 and note in buttonNotesl2):
                buttonId = buttonNotesl2.index(note) 
                # octave 1 -> line 2
                self._handleButtons(2,buttonId,noteOn)
            
            # Encoder groups
            # Top right
            if(octave == 4 and note == "A#"):
                self._handleEncoderGrpButtons("TopRight", noteOn)
            # Bottom right
            if(octave == 3 and note == "D#"):
                self._handleEncoderGrpButtons("BottomRight", noteOn)

            # vPot click
            """ Not yet
            if(octave == 1 and note in knobNotes):
                knobId = knobNotes.index(note)
                print("Knob : "+ str(buttonId+1)+" clicked "+str(noteOn))
            """

            
            

            # Other Buttons
            if(octave == 2):
                if(note == "G#"):
                    self._handleFunctionButtons("F1", noteOn)
                if(note == "G"):
                    self._handleFunctionButtons("F2", noteOn)
                if(note == "F#"):
                    self._handleFunctionButtons("F3", noteOn)
                if(note == "F"):
                    self._handleFunctionButtons("F4", noteOn)

                # Preset / Bank 
                if(note == "A#"):
                    self._handleBankButtons("<", noteOn)
                if(note == "B"):
                    self._handleBankButtons(">", noteOn)
    
            # Four buttons in bottom of the BCF 
            if octave == 6 :
                if(note == "G"):
                    self._handleFunctionButtons("F5", noteOn)
                if(note == "G#"):
                    self._handleFunctionButtons("F6", noteOn)
                if(note == "A"):
                    self._handleFunctionButtons("F7", noteOn)
                if(note == "A#"):
                    self._handleFunctionButtons("F8", noteOn)

        #pitchwheel
        if midiMessage.type == "pitchwheel" :
            self._handlePitchWheel(midiMessage.channel, midiMessage.pitch)
            

    def read(self):
        """ Read Midi message """

        msg = self.midiIN.receive()
        self.routeMessage(msg)

        self.read()


    def _handleButtons(self, line, bId, noteOn):
        """
        Handle the two lines of buttons : Solo / mute or Select / Rec
        """
        address = self.dawConfig.getButtonAddress(line, self.buttonMode)
        value = self.dawConfig.getButtonValue(line, self.buttonMode,noteOn)

        buttonId = (bId +1)+ self.bank*BANK_SIZE
        values = [buttonId, value]
        self.sendOSCMessage(address, values)


    def _handleEncoderGrpButtons(self, name, clicked):
        """
        Handle the Encoder groups button (only top and bottom right)
        """
        if clicked and name == "TopRight" :
            self.buttonMode = "solomute"
        elif clicked and name == "BottomRight":
            self.buttonMode = "selectrec"

        print("button mode: "+self.buttonMode)


    def _handleFunctionButtons(self, name, clicked):
        """
        Handle the function Buttons F1 -> F8    
        """
        print("F Button " + str(name) +" "+str(clicked))
        address = self.dawConfig.getFunctionAddress(name)
        self.sendOSCMessage(address, [])




    def _handleBankButtons(self, name, clicked):
        """
        Handle bank buttons
        """
        print("Bank" + str(name) +" "+str(clicked))
        if clicked and name == ">":
            self.bank = self.bank + 1
        elif clicked and name == "<" and self.bank >0:
            self.bank = self.bank - 1
        print("       >> BANK "+str(self.bank))


    def _handlePitchWheel(self, ch, value):
        """
        Handle fader moves
        """
        faderId = (ch + 1) + self.bank*BANK_SIZE
        
        #TODo convert value to OSC readable
        faderValue = value

        address = self.dawConfig.getFaderAddress()
        values = [faderId, faderValue]

        self.sendOSCMessage(address, values)




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


