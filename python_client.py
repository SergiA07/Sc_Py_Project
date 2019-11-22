"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /control1 address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time
import json

from pythonosc import udp_client

OSC_CONFIG_FILEPATH = './osc_config.json'

if __name__ == "__main__":
    with open(OSC_CONFIG_FILEPATH) as json_file:
        osc_config = json.load(json_file)

    sc_client = udp_client.SimpleUDPClient(
        osc_config["supercollider"]["ip"],
        osc_config["supercollider"]["port"])

    for x in range(100):
        sc_client.send_message("/control1", random.random())
        time.sleep(0.01)
