from os import listdir, getcwd
from os.path import isfile, join
from operator import itemgetter
import codecs
import json

import pandas as pd
import numpy as np
import librosa
import matplotlib.pyplot as plt

# https://musicinformationretrieval.com/kmeans.html
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors


# ------------- constants ------ #
CORPUS_FOLDER_PATH = join(getcwd(), 'sounds')
CONFIG_ANALYSIS_PATH = join(getcwd(),'config/analysis_config.json')
# ------------- constants ------ #


class FeatureAnalyser:
    def __init__(self, corpus_path=CORPUS_FOLDER_PATH):
        # constructor
        self.corpus_path = corpus_path
        self.features_dict = self.compute_feature_dictionaries()

    def is_valid_sound(self, file):
        return isfile(file) and file.lower().endswith(('.wav', '.aiff'))

    def valid_tracks_fullpaths(self, path):
        valid_tracks_fullpaths = []
        tracks_fullpaths = [join(path, track) for track in listdir(path)]

        for path in tracks_fullpaths:
            if self.is_valid_sound(path):
                valid_tracks_fullpaths.append(path)
            else:
                print('invalid format for ', path, ' ,only wav or aiff')
        return valid_tracks_fullpaths

    def add_to_features_dict(self, feature_dict, track_path, feature_values, time_pos):
        for feature_val, time in zip(feature_values, time_pos):
            if feature_val in feature_dict:
                print('repeated value for ', track_path)
            feature_dict[feature_val] = {
                "path": track_path,
                "time_pos": time
            }

    def compute_feature_dictionaries(self):
        with open(CONFIG_ANALYSIS_PATH) as json_file:
            config_analysis = json.load(json_file)

        features_dict = {
                "centroid": {},
                "flatness": {},
            }

        valid_tracks = self.valid_tracks_fullpaths(self.corpus_path)

        for track_path in valid_tracks:
            audio, sr = librosa.load(track_path)

            fft_size, hop_size = itemgetter(
                "fft_size", "hop_size")(config_analysis["centroid"])
            self.add_to_features_dict(
                features_dict["centroid"],
                track_path,
                self.centroid_analize(audio, sr, fft_size, hop_size),
                self.get_frames_time(audio, sr, fft_size, hop_size)
            )

            fft_size, hop_size = itemgetter(
                "fft_size", "hop_size")(config_analysis["flatness"])
            self.add_to_features_dict(
                features_dict["flatness"],
                track_path,
                self.flatness_analize(audio, sr, fft_size, hop_size),
                self.get_frames_time(audio, sr, fft_size, hop_size)
            )

        return features_dict

    def centroid_analize(self, audio, sr, fft_size=2048, hop_size=512):
        centroid_data = librosa.feature.spectral_centroid(
            y=audio, sr=sr, n_fft=fft_size, hop_length=hop_size)
        return centroid_data[0]

    def flatness_analize(self, audio, sr, fft_size=2048, hop_size=512):
        flatness_data = librosa.feature.spectral_flatness(
            y=audio, n_fft=fft_size, hop_length=hop_size)
        return flatness_data[0]

    def get_frames_time(self, audio, sr=22050, fft_size=2048, hop_size=512):
        frames = librosa.samples_to_frames(len(audio), hop_size, fft_size)
        frames_indices = np.arange(frames)
        frame_time_pos = librosa.frames_to_time(
            frames_indices, sr, hop_size, fft_size)
        # ens dona la posició temporal de la meitat de cada frame de 2048 samples
        return frame_time_pos

    def closest(self,keys, K):
        keys = np.asarray(keys)
        index_closest_key = (np.abs(keys - K)).argmin()
        return keys[index_closest_key], index_closest_key

    def get_closest_frame(self, dict_name, K):
        features_dict = self.features_dict[dict_name]
        keys = [*features_dict]
        closest_frame, _ = self.closest(keys, K)
        path = features_dict[closest_frame]["path"]
        time_pos = features_dict[closest_frame]["time_pos"]
        return path, time_pos
