"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse
import math
import json

from pythonosc import dispatcher
from pythonosc import osc_server

OSC_CONFIG_FILEPATH = './osc_config.json'

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass


if __name__ == "__main__":
    with open(OSC_CONFIG_FILEPATH) as json_file:
        osc_config = json.load(json_file)

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", print)
    dispatcher.map("/volume", print_volume_handler, "Volume")
    dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)

    server = osc_server.ThreadingOSCUDPServer(
        (osc_config["python"]["ip"], osc_config["python"]["port"]),
         dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
