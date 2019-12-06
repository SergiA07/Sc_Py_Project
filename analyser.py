


from os import listdir, getcwd
from os.path import isfile, join

import codecs
import json

import pandas as pd
import numpy as np
import librosa
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans #https://musicinformationretrieval.com/kmeans.html
from sklearn.neighbors import NearestNeighbors


# ------------- #

CORPUS_FOLDER_PATH = "/Users/Sergi/Documents/SuperCollider/Proyectos/Lluis/Python_SC_Pde/sounds/"


class Analyser:


    #CORPUS_FOLDER_PATH = join(getcwd(),  "sounds")


    def __init__(self, param1, param2):
        #constructor
        self.param1 = param1
        self.param2 = param2
        self.corpus_path = CORPUS_FOLDER_PATH
        self.dict = self.creator()



    def is_valid_sound(file):
        return isfile(file) and file.lower().endswith(('.wav', '.aiff'))


    def get_valid_tracks(path):
        valid_tracks_fullpaths = []
        tracks_paths = [join(path, track) for track in listdir(path)]

        for path in tracks_paths:
            if is_valid_sound(path):
                valid_tracks_fullpaths.append(path)
            else:
                print('invalid format for ', path, ' ,only wav or aiff')

        return valid_tracks_fullpaths


    def add_to_dict(dict, track_path, features, time_pos):
        for feature, time in zip(features, time_pos):
            dict[feature] = {
                "path" : track_path,
                "time_pos": time
            }


    def creator(self):


        features_dicc = {}
        features_dicc["centroid"] = {}
        features_dicc["flatness"] = {}



        centroid_config = {
            "fft_size": 2048,
            "hop_size": 512
        }

        flatness_config = {
        "fft_size": 2048,
                "hop_size": 512
        }



        valid_tracks = get_valid_tracks(self.corpus_path)



        for track_path in valid_tracks:

            audio, sr = librosa.load(track_path)

            add_to_dict(
                features_dicc["centroid"],
                track_path,
                centroid_analize(audio, sr, centroid_config["fft_size"], centroid_config["hop_size"]),
                get_frames_time(audio, sr, centroid_config["fft_size"], centroid_config["hop_size"])
            )

            add_to_dict(
                features_dicc["flatness"],
                track_path,
                flatness_analize(audio, flatness_config["fft_size"], flatness_config["hop_size"]),
                get_frames_time(audio, sr, flatness_config["fft_size"], flatness_config["hop_size"])
            )

        return features_dicc



    def centroid_analize(audio, sr, fft_size=2048, hop_size=512):
        centroid_data = librosa.feature.spectral_centroid(y=audio, sr=sr, n_fft=fft_size, hop_length=hop_size)
        return centroid_data[0]


    def flatness_analize(audio, fft_size=2048, hop_size=512):
        flatness_data = librosa.feature.spectral_flatness(y=audio, n_fft=fft_size, hop_length=hop_size)
        return flatness_data[0]


    def get_frames_time(audio, sr=22050, fft_size=2048, hop_size=512):
        frames = librosa.samples_to_frames(len(audio),hop_size,fft_size)
        frames_indices = np.arange(frames)
        frame_time_pos = librosa.frames_to_time(frames_indices, sr, hop_size, fft_size)
        #ens dona la posició temporal de la meitat de cada frame de 2048 samples
        return frame_time_pos


    def closest(keys, K):
        keys = np.asarray(keys)
        index_closest_key = (np.abs(keys - K)).argmin()
        return keys[index_closest_key], index_closest_key


    def get_closest_frame(dict_name, K):
        dict = self.dict[dict_name]
        keys = [*dict]
        closest_frame, _ = closest(keys, K)
        path = dict[closest_frame]["path"]
        time_pos = dict[closest_frame]["time_pos"]
        return path, time_pos



    #dict = creator(CORPUS_FOLDER_PATH)

    #path, time_pos = get_closest_frame(dict["flatness"], 0.023456)
