import argparse
import random
import time
import json
from analyser import Analyser

from pythonosc import udp_client

OSC_CONFIG_FILEPATH = './osc_config.json'



def envia():
    # from sc: feature, value
    # from sc: feature, value
    for x in range(100):
        sc_client.send_message("/control1", {'path': random.random(), 'time_pos':random.random()})
        time.sleep(0.01)

if __name__ == "__main__":
    with open(OSC_CONFIG_FILEPATH) as json_file:
        osc_config = json.load(json_file)

    sc_client = udp_client.SimpleUDPClient(
        osc_config["supercollider"]["ip"],
        osc_config["supercollider"]["port"])

    Analisis = Analyser()

    #get_closest('centroid', 0.3546)
    #envia()


# importar analyser
# envia SC com a objecte
