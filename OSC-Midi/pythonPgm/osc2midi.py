"""
This program handle incomming OSC messages to MIDI
"""
import argparse
import random
import time
import json

import sqlite3

import mido
from pythonosc import dispatcher
from pythonosc import osc_server

from lib.midiHelper import *

from sqlalchemy import *


DAW_NAME = "ardour"
CONTROLLER_NAME = "bcf2000"
BANK_SIZE = 8

class OscToMidi:
    def __init__(self, ipAddr, port ):
        self.ipAddr = ipAddr
        self.port = port
        
        self.db = create_engine('sqlite:///midiosc.db')


        # Init Midi client and display available devices
        midiPort = mido.get_output_names()[0]
        self.midiOUT = mido.open_output(midiPort)

        # Get the DAW OSC configuration
        self.dawConfig = DawConfig(DAW_NAME)

        # Get the Controller MIDI configuration
        self.ctrlConfig = ControllerConfig(CONTROLLER_NAME)

        self.buttonMode = "solomute"
        self.bank = 0



        
    def waitForOscMessage(self):
        """
        Wait until osc is received
        """
        self.dispatcher = dispatcher.Dispatcher()
        self._routes()
        server = osc_server.ThreadingOSCUDPServer(
                      (self.ipAddr, self.port), self.dispatcher)
        print("Serving on {}".format(server.server_address))
        # TODO : display this config on OLED displays
        server.serve_forever()



    def _routes(self):
        """
        Route OSC messages to corresponding controller function
        """
        dc = self._dawConfig
        # Faders
        self.dispatcher.map(dc.getFaderAddress(), self._dispatchFader)
        
        # Buttons line1
        self.dispatcher.map(dc.getButtonValue(1, self.buttonMode), self._dispatchButtonsLine1)
        
        # Buttons line2
        self.dispatcher.map(dc.getButtonValue(2, self.buttonMode), self._dispatchButtonsLine2)

        # Function buttons
        for fButton in dc["function"]:
            self.dispatcher.map(dc["function"][fButton], self._dispatchFunctionButtons, fButton )
        
        # Other
        self.dispatcher.map("/debug", print)


    def _dispatchFader(self, address, stripId, faderValue):
        """
        Convert fader OSC value to MIDI value
        """
        faderMidiRange = self._ctrlConfig["fader"]["move"]["valueRange"]
        faderOSCRange = self._dawConfig["strip"]["fader"]["valueRange"]
        faderMove = self._ctrlConfig["fader"]["move"]["type"]
        readyVal = convertValueToMidiRange(faderValue, dawConfig.getFaderOSCRange(), self.ctrlConfig.getFaderMidiRange())
        midiMessage = "{} ch: {} value:{}".format(faderMove, stripId, readyVal)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,faderValue, midiMessage))
        
        msg = mido.Message('pitchwheel', pitch=readyVal, channel=stripId)
        self.midiOUT.send(msg)
        # TODO: handle bank (should be available in database or memory)


    def _dispatchButtonsLine1(self, address, stripId, buttonValue):
        """
        Convert Solo / Rec OSC value to MIDI value
        """
        # TODO: Get surface mode and display accordingly

        # Do nothing if not good mode
        if self.buttonMode == "solomute" and "rec" in address:
            return
        
        buttonsMidiNotes  = self._ctrlConfig["buttons"]["line1"]["notes"]
        buttonsMidiType = self._ctrlConfig["buttons"]["line1"]["type"]
        buttonsMidiOctave = self._ctrlConfig["buttons"]["line1"]["octave"]
        buttonsMidiValueOn = self._ctrlConfig["buttons"]["line1"]["valueOn"]
        buttonsMidiValueOff = self._ctrlConfig["buttons"]["line1"]["valueOff"]
        
        midiNote = midiNoteToNumber(buttonsMidiNotes[stripId],buttonsMidiOctave)
        midiVelocity = buttonsMidiValueOn if buttonValue else buttonsMidiValueOff

        msg = mido.Message(buttonsMidiType, note=midiNote, velocity=midiVelocity)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))
        self.midiOUT.send(msg)


    def _dispatchButtonsLine2(self, address, stripId, buttonValue):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        # TODO: Get surface mode and display accordingly
        
        # Do nothing if not good mode
        if self.buttonMode == "solomute" and "select" in address:
            return

        buttonsMidiNotes  = self._ctrlConfig["buttons"]["line2"]["notes"]
        buttonsMidiType = self._ctrlConfig["buttons"]["line2"]["type"]
        buttonsMidiOctave = self._ctrlConfig["buttons"]["line2"]["octave"]
        buttonsMidiValueOn = self._ctrlConfig["buttons"]["line2"]["valueOn"]
        buttonsMidiValueOff = self._ctrlConfig["buttons"]["line2"]["valueOff"]
        
        midiNote = midiNoteToNumber(buttonsMidiNotes[stripId],buttonsMidiOctave)
        midiVelocity = buttonsMidiValueOn if buttonValue else buttonsMidiValueOff

        msg = mido.Message(buttonsMidiType, note=midiNote, velocity=midiVelocity)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))
        self.midiOUT.send(msg)


    def _dispatchFunctionButtons(self, address, bname):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        bname = bname[0]
        
        fNote  = midiFullNoteToNumber(self._ctrlConfig["fbuttons"][bname]["note"])
        fVelocity = self._ctrlConfig["fbuttons"][bname]["valueOn"]
        fChannel = self._ctrlConfig["fbuttons"][bname]["ch"]
        fType = self._ctrlConfig["fbuttons"][bname]["type"]

        msg = mido.Message(fType, note=fNote, velocity=fVelocity, channel=fChannel)
        print("Dispatching OSC: {} (mapped to {}) to MIDI: {}  ".format(address,bname, msg))
        self.midiOUT.send(msg)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    oscMIDI = OscToMidi(args.ip, args.port)
    
    oscMIDI.waitForOscMessage()
