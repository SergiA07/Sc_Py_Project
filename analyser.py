import os
from os import listdir, getcwd
from os.path import isfile, join, normpath
from operator import itemgetter
import codecs
import simplejson as json
import math
# import json

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

    def add_to_features_dict(self, feature_dict, track_path, feature_values, time_pos, fft_size, hop_size, sample_rate):
        for feature_val, time in zip(feature_values, time_pos):
            if feature_val in feature_dict:
                print('repeated value for ', track_path)
            feature_dict[feature_val] = {
                "path": track_path,
                "time_pos": time,
                "fft_size": fft_size,
                "hop_size": hop_size,
                "sample_rate": sample_rate
            }

    def compute_feature_dictionaries(self):
        with open(CONFIG_ANALYSIS_PATH) as f:
            config_analysis = json.load(f)

        features_dict = {}
        for feature_name in config_analysis.keys():
            features_dict[feature_name] = {}

        valid_tracks, tracks_names = self.valid_tracks_fullpaths()

        for track_path, track_name in zip(valid_tracks, tracks_names):
            for feature_name, feature_config_analisis in config_analysis.items():

                fft_size, hop_size, sample_rate = itemgetter("fft_size", "hop_size", "sample_rate")(feature_config_analisis)
                feature_folder = join(FEATURES_FILEPATH, feature_name + '_' + str(fft_size) + '_' + str(hop_size) + '_' + str(sample_rate))
                #feature_folder = join(FEATURES_FILEPATH, feature_name)

                feature_analisis_json = join(
                    feature_folder, track_name + '.json')

                # if not precomupted, compute feature:
                if not os.path.exists(feature_analisis_json):
                    self.create_feature_analisis_json(
                        feature_name, feature_config_analisis, track_path, feature_analisis_json)
                    print("computat", track_name, feature_name)

                # load analisis from precomputed json
                with open(feature_analisis_json) as f:
                    feature_analisis, time_pos = itemgetter(
                        "feature_analisis", "time_pos")(json.load(f))
                    print("carregat", track_name, feature_name)

                self.add_to_features_dict(
                    features_dict[feature_name],
                    track_path,
                    feature_analisis,
                    time_pos,
                    fft_size,
                    hop_size,
                    sample_rate
                )
        return features_dict

    def create_feature_analisis_json(self, feature_name, feature_config_analisis, track_path, json_to_save_name):
        def normalise_audio(audio, hop_size):
            '''performs tranformations to obtain a correct audio to analise:
            - only use left channel on stereo signals
            - discard last samples if the don't fill a whole frame
            '''
            if len(audio.shape) > 1:
                audio = audio[0]  # only left channel
            audio = np.asfortranarray(audio)  # otherwise some errors
            exact_size = math.floor(len(audio)/hop_size) * hop_size
            audio = audio[:exact_size]  # remove last samples if needed
            return audio

        def get_frame_time_positions(feature_analisis_results, sr, hop_size=512):
            '''returns an array containing the time position at the start of each frame'''
            frames_indices = np.arange(len(feature_analisis_results))
            frame_time_pos = librosa.frames_to_time(
                frames_indices, sr, hop_size)
            return frame_time_pos

        fft_size, hop_size, sample_rate = itemgetter(
            "fft_size", "hop_size", "sample_rate")(feature_config_analisis)
        audio, sr = librosa.load(track_path, sr=sample_rate, mono=False)
        audio = normalise_audio(audio, hop_size)

        function = getattr(self, feature_name + '_analiser')
        feature_analisis = function(audio, sr, fft_size, hop_size)
        time_pos = get_frame_time_positions(feature_analisis, sr, hop_size)

        feature_folder = join(FEATURES_FILEPATH, feature_name + '_' + str(fft_size) + '_' + str(hop_size) + '_' + str(sample_rate))
        #feature_folder = join(FEATURES_FILEPATH, feature_name)
        if not os.path.exists(feature_folder):
            os.makedirs(feature_folder)
        with open(json_to_save_name, 'w') as f:
            json.dump({'feature_analisis': feature_analisis.tolist(
            ), 'time_pos': time_pos.tolist()}, f)  # save as json

    ''' ======= ANALISIS FUNCTIONS: they must follow the naming {my_analisis}_analiser =============='''

    def centroid_analiser(self, audio, sr, fft_size=2048, hop_size=512):
        centroid_data = librosa.feature.spectral_centroid(
            y=audio, sr=sr, n_fft=fft_size, hop_length=hop_size, center=False)
        return centroid_data[0]

    def flatness_analiser(self, audio, sr, fft_size=2048, hop_size=512):
        flatness_data = librosa.feature.spectral_flatness(
            y=audio, n_fft=fft_size, hop_length=hop_size, center=False)
        return flatness_data[0]
    '''============================================================================'''

    def get_closest_frame(self, feature_name, target_value):
        def closest(keys, target_value):
            keys = np.asarray(keys)
            index_closest_key = (np.abs(keys - target_value)).argmin()
            return keys[index_closest_key], index_closest_key
        features_dict = self.features_dict[feature_name]
        keys = [*features_dict]
        closest_frame, _ = closest(keys, target_value)
        path = features_dict[closest_frame]["path"]
        time_pos = features_dict[closest_frame]["time_pos"]
        start_sample = time_pos * features_dict[closest_frame]["sample_rate"]
        frame_dur = features_dict[closest_frame]["fft_size"] /features_dict[closest_frame]["sample_rate"]
        print(path)
        print(start_sample)
        print(frame_dur)
        return path, start_sample, frame_dur
