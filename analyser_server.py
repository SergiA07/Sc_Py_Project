from os import listdir, getcwd
from os.path import isfile, join
import argparse
import math
import random
import time
import json
from analyser import FeatureAnalyser

from pythonosc import udp_client

from pythonosc import dispatcher
from pythonosc import osc_server

# ------------- constants ------ #
OSC_CONFIG_FILEPATH = join(getcwd(), 'config/osc_config.json')
# ------------- constants ------ #


def receive_send_data(address, *args):
    feature = args[0]
    valor = args[1]
    frame_path, frame_start_sample, frame_dur = analisis.get_closest_frame(
        feature, valor)
    sc_client.send_message(
        "/data", [frame_path, frame_start_sample, frame_dur, feature])


def handle_audio_paths_request(address, *args):
    audio_full_paths, _ = analisis.valid_tracks_fullpaths()
    sc_client.send_message("/audio_paths", audio_full_paths)


if __name__ == "__main__":
    analisis = FeatureAnalyser()

    with open(OSC_CONFIG_FILEPATH) as json_file:
        osc_config = json.load(json_file)

    sc_client = udp_client.SimpleUDPClient(
        osc_config["supercollider"]["ip"],
        osc_config["supercollider"]["port"])

    processing_client = udp_client.SimpleUDPClient(
        osc_config["processing"]["ip"],
        osc_config["processing"]["port"])

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/data", receive_send_data)
    dispatcher.map("/audio_paths", handle_audio_paths_request)

    server = osc_server.ThreadingOSCUDPServer(
        (osc_config["python"]["ip"], osc_config["python"]["port"]),
        dispatcher)
    print("Serving on {}".format(server.server_address))

    # print(analisis.features_dict)

    #features_info = analisis.send_features_info(sublists_size=8)
    # for index in range(len(features_info)):
    #    for index2, elem in enumerate(features_info[index]):
    #        if index2 != 0:
    #            for array in elem:
    #                print(array)
    #                print("")
    #        else:
    #            print(elem)
    #            print("")
    #processing_client.send_message("/test", x)

    audio_full_paths, _ = analisis.valid_tracks_fullpaths()
    sc_client.send_message("/audio_paths", audio_full_paths)

    server.serve_forever()
