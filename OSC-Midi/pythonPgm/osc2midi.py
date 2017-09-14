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
from pythonosc import osc_message_builder
from pythonosc import udp_client



from lib.midiHelper import *
from lib.database import Database

from mappings.mapping import ControllerConfig, DawConfig


class OscToMidi:
    def __init__(self, ipAddr, port ):
        self.ipAddr = ipAddr
        self.port = port
        
        self.db = Database()

        # Init Midi client and display available devices
        midiPort = mido.get_output_names()[0]
        self.midiOUT = mido.open_output(midiPort)

        # Get the DAW OSC configuration
        self.dawConfig = DawConfig(self.db.getDawName())

        # Get the Controller MIDI configuration
        self.ctrlConfig = ControllerConfig(self.db.getControllerName())

        
    def waitForOscMessage(self):
        """
        Wait until osc is received
        """
        self.dispatcher = dispatcher.Dispatcher()
        self._routes()

        oscClient = udp_client.UDPClient("127.0.0.1",3128 )
        msg = osc_message_builder.OscMessageBuilder(address = "/set_surface/feedback")
        msg.add_arg(4087)
        oscClient.send(msg.build())

        server = osc_server.ThreadingOSCUDPServer(
                      (self.ipAddr, self.port), self.dispatcher)
        print("Serving on {}".format(server.server_address))
        # TODO : display this config on OLED displays
        server.serve_forever()



    def _routes(self):
        """
        Route OSC messages to corresponding controller function
        """
        dc = self.dawConfig
        buttonMode = self.db.getButtonMode()

        # Faders
        self.dispatcher.map(dc.getFaderAddress(), self._dispatchFader)
        
        # Buttons line1
        self.dispatcher.map(dc.getButtonAddress(1, buttonMode), self._dispatchButtonsLine1)
        
        # Buttons line2
        self.dispatcher.map(dc.getButtonAddress(2, buttonMode), self._dispatchButtonsLine2)

        """
        # Function buttons
        for fButton in dc.getFunctionAddress():
            self.dispatcher.map(dc.getFunctionAddress(fButton), self._dispatchFunctionButtons, fButton )
        """

        # Other
        self.dispatcher.map("/debug", print)


    def _dispatchFader(self, address, stripId, faderValue):
        """
        Convert fader OSC value to MIDI value
        """
        faderMidiRange = self.ctrlConfig.getFaderMidiRange()
        faderOSCRange = self.dawConfig.getFaderOSCRange()
        faderMove = self.ctrlConfig.getFaderMove("type")
        readyVal = convertValueToMidiRange(faderValue, self.dawConfig.getFaderOSCRange(), self.ctrlConfig.getFaderMidiRange())
        
        # TODO: handle bank (should be available in database or memory)
        # stripId with bank handle
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()
        
        sId = stripId

        # need to stay in 1 -> bankSize range
        if(sId > bankSize):
            sId = (sId % bankSize) +1


        midiMessage = "{} ch: {} value:{}".format(faderMove, sId, readyVal)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,faderValue, midiMessage))
        
        msg = mido.Message('pitchwheel', pitch=readyVal, channel=sId)
        self.midiOUT.send(msg)


    def _dispatchButtonsLine1(self, address, stripId, buttonValue):
        """
        Convert Solo / Rec OSC value to MIDI value
        """
        # Do nothing if not good mode
        buttonMode = self.db.getButtonMode()
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()

        if buttonMode == "solomute" and "rec" in address:
            return
    
        line = 1
        buttonsMidiNotes  = self.ctrlConfig.getButtonNotes(line)
        buttonsMidiType = self.ctrlConfig.getButtonType(line)

        sId = stripId -1
        # need to stay in 1 -> bankSize range
        if(sId >= bankSize):
            sId = (sId % bankSize) 

        midiNote = midiFullNoteToNumber(buttonsMidiNotes[sId])
        midiVelocity = 127 #buttonsMidiValueOn if buttonValue else buttonsMidiValueOff
        msg = mido.Message(buttonsMidiType, note=midiNote, velocity=midiVelocity)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))
        self.midiOUT.send(msg)


    def _dispatchButtonsLine2(self, address, stripId, buttonValue):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        buttonMode = self.db.getButtonMode()
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()

        # Do nothing if not good mode
        if buttonMode == "solomute" and "select" in address:
            return
        
        line = 2
        buttonsMidiNotes  = self.ctrlConfig.getButtonNotes(line)
        buttonsMidiType = self.ctrlConfig.getButtonType(line)
 
        sId = stripId - 1
        # need to stay in 1 -> bankSize range
        if(sId >= bankSize):
            sId = (sId % bankSize) 

        midiNote = midiFullNoteToNumber(buttonsMidiNotes[sId])

        midiVelocity = 127 #buttonsMidiValueOn if buttonValue else buttonsMidiValueOff
        msg = mido.Message(buttonsMidiType, note=midiNote, velocity=midiVelocity)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))
        self.midiOUT.send(msg)


    def _dispatchFunctionButtons(self, address, bname):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        bname = bname[0]
        
        fNote  = midiFullNoteToNumber(self.ctrlConfig.getfButtonNote(bname,"note"))
        fVelocity = self.ctrlConfig.getfButtonNote(bname,"valueOn")
        fChannel = self.ctrlConfig.getfButtonNote(bname,"ch")
        fType = self.ctrlConfig.getfButtonNote(bname,"type")

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
