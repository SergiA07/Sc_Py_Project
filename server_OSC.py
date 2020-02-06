from os import getcwd
from os.path import join
import json

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

# ------------- constants ------ #
OSC_CONFIG_FILEPATH = join(getcwd(), 'config/osc_config.json')
# ------------- constants ------ #


class server_OSC:
    def receive_send_data(self, address, *args):
        feature = args[0]
        valor = args[1]
        frame_path, frame_start_sample, frame_dur = self.analysis.get_closest_frame(
            feature, valor)
        self.sc_client.send_message(
            "/data", [frame_path, frame_start_sample, frame_dur, feature])

    def handle_audio_paths_request(self, address, *args):
        audio_full_paths, _ = self.analysis.valid_tracks_fullpaths()
        self.sc_client.send_message("/audio_paths", audio_full_paths)

    def __init__(self, analysis):
        with open(OSC_CONFIG_FILEPATH) as json_file:
            osc_config = json.load(json_file)

        self.analysis = analysis
        self.sc_client = udp_client.SimpleUDPClient(
            osc_config["supercollider"]["ip"],
            osc_config["supercollider"]["port"])
        self.processing_client = udp_client.SimpleUDPClient(
            osc_config["processing"]["ip"],
            osc_config["processing"]["port"])

        osc_dispatcher = dispatcher.Dispatcher()
        osc_dispatcher.map("/data", self.receive_send_data)
        osc_dispatcher.map("/audio_paths", self.handle_audio_paths_request)

        server = osc_server.ThreadingOSCUDPServer(
            (osc_config["python"]["ip"], osc_config["python"]["port"]),
            osc_dispatcher)
        print("Serving on {}".format(server.server_address))

        # print(analysis.features_dict)

        audio_full_paths, _ = analysis.valid_tracks_fullpaths()
        self.sc_client.send_message("/audio_paths", audio_full_paths)
        server.serve_forever()
