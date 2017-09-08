"""

"""
import argparse
import random
import time
import json

import sqlite3

import mido
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from sqlalchemy import *


DAW_NAME = "ardour"

class OscToMidi:
    def __init__(self, ipAddr, port ):
        self.ipAddr = ipAddr
        self.port = port
        
        self.db = create_engine('sqlite:///midiosc.db')


        # Init Midi client and display available devices
        midiPort = mido.get_input_names()[0]
        self.midiIN = mido.open_input(midiPort)

        # Get the DAW OSC configuration
        with open('dawConfig/'+DAW_NAME+'.json', 'r') as f:
            self._dawConfig = json.load(f)

        
    def waitForOscMessage(self):
        """
        Wait until osc is received
        """
        self.dispatcher = dispatcher.Dispatcher()
        server = osc_server.ThreadingOSCUDPServer(
                      (self.ipAddr, self.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()
        pass



    def routes(self):
        dc = self._dawConfig
        self.dispatcher.map("/debug", print)

        self.dispatcher.map(dc.strip.fader, print)





    def sendMidi(self, message):
        pass











if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    oscMIDI = OscToMidi(args.ip, args.port)
    
    oscMIDI.waitForOscMessage()
