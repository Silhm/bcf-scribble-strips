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
        with open('mappings/daw-osc/'+DAW_NAME+'.json', 'r') as f:
            self._dawConfig = json.load(f)
               
        # Get the Controller MIDI configuration
        with open('mappings/controllers/'+CONTROLLER_NAME+'.json', 'r') as f2:
            self._ctrlConfig = json.load(f2)


        self.buttonMode = "solomute"
        self.bank = 0


        """
        TODO
            wait for OSC
            route OSC message
            save configs to a database
            convert it to MIDI
            send midi
            profit!
        """


        
    def waitForOscMessage(self):
        """
        Wait until osc is received
        """
        self.dispatcher = dispatcher.Dispatcher()
        self._routes()
        server = osc_server.ThreadingOSCUDPServer(
                      (self.ipAddr, self.port), self.dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()



    def _routes(self):
        dc = self._dawConfig
        # get all necessary osc Address to change controller state
        #faders
        self.dispatcher.map(dc["strip"]["fader"]["address"], self._dispatchFader)
        
        #buttons line1
        self.dispatcher.map(dc["strip"]["solo"]["address"], self._dispatchButtonsLine1)
        self.dispatcher.map(dc["strip"]["select"]["address"] , self._dispatchButtonsLine1)
        
        #buttons line2
        self.dispatcher.map(dc["strip"]["mute"]["address"], self._dispatchButtonsLine2)
        self.dispatcher.map(dc["strip"]["rec"]["address"], self._dispatchButtonsLine2)

        #function buttons
        for fButton in dc["function"]:
            self.dispatcher.map(dc["function"][fButton], self._dispatchFunctionButtons, fButton )
        
        
        self.dispatcher.map("/debug", print)




    def _dispatchFader(self, address, stripId, faderValue):
        """
        Convert fader OSC value to MIDI value
        """
        faderMidiRange = self._ctrlConfig["fader"]["move"]["valueRange"]
        faderOSCRange = self._dawConfig["strip"]["fader"]["valueRange"]
        faderMove = self._ctrlConfig["fader"]["move"]["type"]
        readyVal = self.convertValueToMidiRange(faderValue, faderOSCRange, faderMidiRange)
        midiMessage = "{} ch: {} value:{}".format(faderMove, stripId, readyVal)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,faderValue, midiMessage))
        
        msg = mido.Message('pitchwheel', pitch=readyVal, channel=stripId)
        self.midiOUT.send(msg)
        # TODO: handle bank


    def _dispatchButtonsLine1(self, address, stripId, buttonValue):
        """
        Convert Solo / Rec OSC value to MIDI value
        """
        #Get surface mode and display accordingly

        #Do nothing if not good mode
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
        self.midiOUT.send(msg)

        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))




    def _dispatchButtonsLine2(self, address, stripId, buttonValue):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        #Get surface mode and display accordingly
        
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
        self.midiOUT.send(msg)
        
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))
    


    def _dispatchFunctionButtons(self, address, bname):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        bname = bname[0]
        #midiFullNoteToNumber()
        
        fNote  = midiFullNoteToNumber(self._ctrlConfig["fbuttons"][bname]["note"])
        fVelocity = self._ctrlConfig["fbuttons"][bname]["valueOn"]
        fChannel = self._ctrlConfig["fbuttons"][bname]["ch"]
        fType = self._ctrlConfig["fbuttons"][bname]["type"]

        msg = mido.Message(fType, note=fNote, velocity=fVelocity, channel=fChannel)
        self.midiOUT.send(msg)

        print("Dispatching OSC: {} (mapped to {}) to MIDI: {}  ".format(address,bname, msg))




    def convertValueToMidiRange(self, oscValue, oscRange, midiRange):
        """
        value : OSC value
        OscRange: 
        midiRange
        """        
        minOSC = oscRange[0]
        maxOSC = oscRange[1]

        minMidi = midiRange[0]
        maxMidi = midiRange[1]

        percent = (oscValue - minOSC ) / (maxOSC-minOSC) * 100.0
        midiVal = (maxMidi - minMidi) * percent  / 100 + minMidi

        return int(midiVal)








if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    oscMIDI = OscToMidi(args.ip, args.port)
    
    oscMIDI.waitForOscMessage()
