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
from lib.database import Database

from mappings.mapping import ControllerConfig, DawConfig


class MidiToOSC:

    def __init__(self, ipAddr=None, port=None ):

        self.db = Database()

        ipAddr = self.db.getDawIpAddress() if not ipAddr else ipAddr
        port = self.db.getDawPort() if not port else port

        # Init OSC client
        print("OSC will be sent on "+ipAddr+":"+str(port)) 
        self._oscClient = udp_client.UDPClient(ipAddr, port)

        # Init Midi client and display available devices
        midiPort = mido.get_input_names()[0]
        self.midiIN = mido.open_input(midiPort)


        # Get the DAW OSC configuration
        self.dawConfig = DawConfig(self.db.getDawName())

        # Get the Controller MIDI configuration
        self.ctrlConfig = ControllerConfig(self.db.getControllerName())

        self._faderPos = {}


    def sendOSCMessage(self, address, values):
        """
        Send the corresponding OSC message
            - address is a string
            - value is an array
        """
        msg = osc_message_builder.OscMessageBuilder(address = address)
        
        for arg in values:
            msg.add_arg(arg)

        print(">        OSC: {} {}".format(address,values))
        self._oscClient.send(msg.build())



    def routeMessage(self, midiMessage):
        """
        Route midi message to the correct OSC address
        """
        print("MIDI message: {}".format(midiMessage))
        
        faderNotes = self.ctrlConfig.getFaderNotes()
        vPotNotes = self.ctrlConfig.getVpotButtonNotes()
        vPotCC = self.ctrlConfig.getVpotCC()
        buttonNotes = self.ctrlConfig.getButtonNotes(1) # line1
        buttonNotesl2 = self.ctrlConfig.getButtonNotes(2) # line2
        
        fButtonNotes = self.ctrlConfig.getfButtonNotes()
        bankButtonNotes = self.ctrlConfig.getBankButtonNotes()
 

        if midiMessage.type == "note_on":
            midiNote = midiNumberToFullNote(midiMessage.note)


        # Fader moves : Pitchwheel 
        if midiMessage.type == "pitchwheel" :
            self._handlePitchWheel(midiMessage.channel, midiMessage.pitch)
            faderValue = convertValueToOSCRange(midiMessage.pitch, self.dawConfig.getFaderOSCRange(), self.ctrlConfig.getFaderMidiRange())
            self._faderPos[midiMessage.channel+1] = faderValue


        # Fader touched
        if(midiMessage.type == "note_on" and midiNote in faderNotes):
            noteOn = midiMessage.type == "note_on" and midiMessage.velocity == 127
            faderId = faderNotes.index(midiNote)+1
            #print("Fader "+ str(faderId)+" touched! "+str(noteOn))
            if noteOn == False:
                #save the last pitchwheel know in db
                self.db.setFaderPosition(faderId, self._faderPos[faderId])


        # NOTE ON
        noteOn = midiMessage.type == "note_on" and midiMessage.velocity == 127
        # TODO : toggle not on/off with one click with dbState
        if noteOn: #or midiMessage.type == "note_off":
            if(midiMessage.velocity == 0):
                return

            # Buttons first and second line
            if(midiNote in buttonNotes):
                buttonId = buttonNotes.index(midiNote)
                self._handleButtons(1,buttonId,noteOn)
            elif(midiNote in buttonNotesl2):
                buttonId = buttonNotesl2.index(midiNote)
                self._handleButtons(2,buttonId,noteOn)
 
            # vPot click
            if(midiNote in vPotNotes):
                vPotId = vPotNotes.index(midiNote)+1
                self._handleVpotClick(vPotId, noteOn)
            

            # Encoder groups : only 2 of 4 are working... need investigation
            # Top right
            if(midiNote == "A#4"):
                self._handleEncoderGrpButtons("TopRight", noteOn)
            # Bottom right
            if(midiNote == "D#3"):
                self._handleEncoderGrpButtons("BottomRight", noteOn)
           
            # Function Buttons
            if(midiNote in fButtonNotes):
                fId = "F{}".format(fButtonNotes.index(midiNote)+1)
                self._handleFunctionButtons(fId, noteOn)
            
            # Preset / Bank buttons
            if(midiNote in bankButtonNotes):
                updown = "up" if bankButtonNotes.index(midiNote) == 0 else "down"
                self._handleBankButtons(updown, noteOn)

        # CC
        elif midiMessage.type == "control_change":
            cc  = midiMessage.control
            val = midiMessage.value
    
            if(cc in vPotCC):
                vPotId = vPotCC.index(cc) + 1
                self._handleVpotRot(vPotId,val)


    def read(self):
        """ Read Midi message """

        msg = self.midiIN.receive()
        self.routeMessage(msg)

        return msg
        

    def _handleButtons(self, line, bId, noteOn):
        """
        Handle the two lines of buttons : Solo / mute or Select / Rec
        """
        buttonMode = self.db.getButtonMode()
        address = self.dawConfig.getButtonAddress(line, buttonMode)

        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()

        # Handle toggle state by getting current state in DB
        dbVal = self.db.getButtonState(line, bId, buttonMode)
        value = self.dawConfig.getButtonValue(line, buttonMode, not dbVal)

        # Save it in the database:
        self.db.setButtonState(line, bId, buttonMode, value)


        buttonId = (bId +1)+ bank*bankSize
        values = [buttonId, value]
        self.sendOSCMessage(address, values)


    def _handleEncoderGrpButtons(self, name, clicked):
        """
        Handle the Encoder groups button (only top and bottom right)
        """
        # Write this in database
        if clicked and name == "TopRight" :
            self.db.setButtonMode("solomute")
        elif clicked and name == "BottomRight":
            self.db.setButtonMode("selectrec")

        print("button mode: {}".format(self.db.getButtonMode()))


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
        bank = self.db.getCurrentBank()

        if clicked and name == "up":
            self.db.bankUp()
        elif clicked and name == "down" and bank >0:
            self.db.bankDown()
        bank = self.db.getCurrentBank()
        print("       >> BANK "+str(bank))


    def _handlePitchWheel(self, ch, value):
        """
        Handle fader moves
        """
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()

        faderId = ch  + bank*bankSize
        
        faderValue = convertValueToOSCRange(value, self.dawConfig.getFaderOSCRange(), self.ctrlConfig.getFaderMidiRange())

        address = self.dawConfig.getFaderAddress()
        values = [faderId+1, faderValue]
    
        self.sendOSCMessage(address, values)


    def _handleVpotClick(self, id, clicked):
        """
        Handle vPot click: restore default pan or gain
        """
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()
        
        vPotMode = self.db.getVpotMode()
            
        vPotId = id + (bank * bankSize)

        address = self.dawConfig.getVpotAddress(vPotMode)

        val = 0.5 if vPotMode == "pan" else 666

        self.db.setvPotValue(vPotId, vPotMode, val)

        values = [vPotId, val]
        self.sendOSCMessage(address, values)
 

    def _handleVpotRot(self, id, value):
        """
        Handle vPot rotation 
        """
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()

        vPotId = id + (bank * bankSize)
        rotation = self.ctrlConfig.getVpotRotation(value)

        # > get the pot mode first
        vPotMode = self.db.getVpotMode()
        address = self.dawConfig.getVpotAddress(vPotMode)
        valueRange = self.dawConfig.getvPotOSCRange(vPotMode)
        # > Get the last Position known for this vPot (according to mode)
        currentVal = self.db.getvPotValue(id, vPotMode)
        # > change it according to direction and speed
        direction = 1 if rotation[0]=="CW" else -1
        speed= rotation[1] if rotation[1]>1 else 1
        _speeds = [10, 3, 2, 2, 1, 1, 1, 1, 1 , 1]

        newVal = currentVal + (direction * 5 * (pow(10, -1 * _speeds[speed]  )))
        if newVal > valueRange[1]:
            newVal = valueRange[1]
        if newVal < valueRange[0]:
            newVal = valueRange[0]

        # > Save it to the database
        self.db.setvPotValue(id, vPotMode, newVal)
        
        values = [id,newVal]
        # > Send it as OSC message!
        self.sendOSCMessage(address, values)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=None,
        help="The ip of the DAW OSC server")
    parser.add_argument("--port", type=int, default=None,
        help="The port the DAW OSC is listening to")
    args = parser.parse_args()

    midiOSC = MidiToOSC(args.ip, args.port)

    # Read Midi
    print("Read midi input...")

    while midiOSC.read():
        pass


