"""
make everything work together!
"""
import argparse
import subprocess

from midi2osc import MidiToOSC
from osc2midi import OscToMidi

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    midiOSCProc = subprocess.Popen(["python3","midi2osc.py"])  #MidiToOSC(args.ip, args.port)
    midiOSCProc.wait()

    #oscMIDIProc = #OscToMidi(args.ip, args.port)

