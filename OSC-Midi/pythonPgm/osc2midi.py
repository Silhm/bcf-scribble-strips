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
        midiPort = mido.get_input_names()[0]
        self.midiIN = mido.open_input(midiPort)

        # Get the DAW OSC configuration
        with open('mappings/daw-osc/'+DAW_NAME+'.json', 'r') as f:
            self._dawConfig = json.load(f)
               
        # Get the Controller MIDI configuration
        with open('mappings/controllers/'+CONTROLLER_NAME+'.json', 'r') as f2:
            self._ctrlConfig = json.load(f2)


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
        """
        self.dispatcher.map(dc["strip"]["fader"]["address"], self._dispatchFader)

        #buttons line1
        self.dispatcher.map(dc["strip"]["solo"]["address"], self._dispatchButtons)
        self.dispatcher.map(dc["strip"]["select"]["address"] , self._dispatchButtons)

        #buttons line2
        self.dispatcher.map(dc["strip"]["mute"]["address"], self._dispatchButtons)
        self.dispatcher.map(dc["strip"]["rec"]["address"], self._dispatchButtons)

        #function buttons
        #TODO
        """
        
        
        
        self.dispatcher.map("/debug", print)




    def _dispatchFader(self, address, stripId, faderValue):
        # convert fader OSC value to MIDI value
        faderMidiRange = self._ctrlConfig["fader"]["move"]["valueRange"]
        faderOSCRange = self._dawConfig["strip"]["fader"]["valueRange"]

        faderMove = self._ctrlConfig["fader"]["move"]["type"]
       
        readyVal = self.convertValueToMidiRange(faderValue, faderOSCRange, faderMidiRange)
        
        midiMessage = "{} ch: {} value:{}".format(faderMove, stripId, readyVal)
            
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,faderValue, midiMessage))
        # TODO: handle bank


    def _dispatchButtons(self, args):
        print("dispatch button message")
        #Get surface mode and display accordingly
        print(args)


    def sendMidi(self, message):
        pass


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
