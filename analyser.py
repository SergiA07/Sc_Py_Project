import os
from os import listdir, getcwd
from os.path import isfile, join, normpath
from operator import itemgetter
import codecs
import simplejson as json
#import json

import pandas as pd
import numpy as np
import librosa
import matplotlib.pyplot as plt

# https://musicinformationretrieval.com/kmeans.html
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors


# ------------- constants ------ #
CORPUS_FOLDER_PATH = join(getcwd(), 'sounds')
CONFIG_ANALYSIS_PATH = join(getcwd(), 'config/analysis_config.json')
FEATURES_FILEPATH = join(getcwd(), 'features/')
# ------------- constants ------ #


class FeatureAnalyser:
    def __init__(self, corpus_path=CORPUS_FOLDER_PATH):
        # constructor
        self.corpus_path = corpus_path
        self.features_dict = self.compute_feature_dictionaries()

    def is_valid_sound(self, file):
        return isfile(file) and file.lower().endswith(('.wav', '.aiff'))

    def valid_tracks_fullpaths(self):
        path = self.corpus_path
        valid_tracks_fullpaths = []
        tracks_names = []
        tracks_fullpaths = [join(path, track) for track in listdir(path)]

        for path, name in zip(tracks_fullpaths, listdir(path)):
            if self.is_valid_sound(path):
                valid_tracks_fullpaths.append(path)
                tracks_names.append(name)
            else:
                print('invalid format for ', path, ' ,only wav or aiff')
        return valid_tracks_fullpaths, tracks_names

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

        features_dict = {}
        for feature_name in config_analysis.keys():
            features_dict[feature_name] = {}

        valid_tracks, tracks_names = self.valid_tracks_fullpaths()

        for track_path, track_name in zip(valid_tracks, tracks_names):
            for feature_name in config_analysis.keys():
                feature_folder = join(FEATURES_FILEPATH, feature_name)
                feature_analisis_json = join(
                    feature_folder, track_name + '.json')
            # if precomupted
                if os.path.exists(feature_analisis_json):
                    with open(feature_analisis_json) as json_file:
                        analisis = json.load(json_file)
                        feature_analisis, time_pos = itemgetter(
                            "feature_analisis", "time_pos")(analisis)
                        print("carregat", track_name, feature_name)
                else:
                    # else compute
                    audio, sr = librosa.load(track_path, mono=False)
                    audio = audio[0]  # només agafem el canal esquerra
                    fft_size, hop_size = itemgetter(
                        "fft_size", "hop_size")(config_analysis[feature_name])
                    function = getattr(self, feature_name + '_analize')
                    feature_analisis = function(audio, sr, fft_size, hop_size)
                    time_pos = self.get_frames_time(
                        audio, sr, fft_size, hop_size)

                    if not os.path.exists(feature_folder):
                        os.makedirs(feature_folder)

                    with open(feature_analisis_json, 'w') as f:
                        json.dump({'feature_analisis': feature_analisis.tolist(
                        ), 'time_pos': time_pos.tolist()}, f)
                    print("computat", track_name, feature_name)
            self.add_to_features_dict(
                features_dict[feature_name],
                track_path,
                feature_analisis,
                time_pos
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

    def closest(self, keys, K):
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
