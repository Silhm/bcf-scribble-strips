"""
This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import osc_message_builder
from pythonosc import udp_client

def random_bool():
  return int(random.random() * 10)%2

def random_name():
    items = ["Kick","Snare","Bass", "Guitar","Vox", "Synths", "Orchestra"]
    return random.choice(items)

def random_float():
    return random.random()

def random_int():
    return int(random.random() * 10)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=8000,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.UDPClient(args.ip, args.port)

  for x in range(10): 
    val = int(random.random() * 10)
    print("sending "+ str(val%2) )

    stripMsg = osc_message_builder.OscMessageBuilder(address = "/strip/name")
    #stripMsg = osc_message_builder.OscMessageBuilder(address = "/debug")
    stripMsg.add_arg(8)
    stripMsg.add_arg(random_name())
    stripMsg = stripMsg.build()
    client.send(stripMsg)

    stripMsg = osc_message_builder.OscMessageBuilder(address = "/strip/mute")
    stripMsg.add_arg(8)
    stripMsg.add_arg(random_bool())
    stripMsg = stripMsg.build()
    client.send(stripMsg)

    stripMsg = osc_message_builder.OscMessageBuilder(address = "/strip/solo")
    stripMsg.add_arg(8)
    stripMsg.add_arg(random_bool())
    stripMsg = stripMsg.build()
    client.send(stripMsg)

    stripMsg = osc_message_builder.OscMessageBuilder(address = "/strip/pan_stereo_position")
    stripMsg.add_arg(8)
    stripMsg.add_arg(random_float())
    stripMsg = stripMsg.build()
    client.send(stripMsg)











    time.sleep(0.3)

    


