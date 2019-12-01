from os import listdir
from os.path import isfile, join

import codecs
import json

import pandas as pd
import numpy as np
import librosa
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans #https://musicinformationretrieval.com/kmeans.html
from sklearn.neighbors import NearestNeighbors


# ----------- #

#CORPUS_FOLDER_PATH = join(getcwd(),  "sounds")

CORPUS_FOLDER_PATH = "/Users/Sergi/Desktop/carpeta sense nom/sounds/"

# ----------- #


def is_valid_sound(file):
    return isfile(file) and file.lower().endswith(('.wav', '.aiff'))


def track_info_creator(track_name, folder_path):

    track_info = {}
    track_name = track_name.split("/")
    track_name = track_name[-1]
    track_info["track_id"] = track_name
    track_info["absolute_path"] = join(folder_path, track_name)
    return track_info


def tracks_info(sound_files_path):

    valid_tracks_fullpaths = []
    tracks_paths = [join(sound_files_path, track) for track in listdir(sound_files_path)]

    for path in tracks_paths:
        if is_valid_sound(path):
            valid_tracks_fullpaths.append(path)
        else:
            print('invalid format for ', path, ' ,only wav or aiff')

    tracks_info = [track_info_creator(track, sound_files_path) for track in valid_tracks_fullpaths]
    return tracks_info, valid_tracks_fullpaths

    # df =  pd.DataFrame([track_info_creator(tr, sound_files_path) for tr in valid_tracks])
    # df.sort_values('track_id', inplace=True) #sort alphabetically
    # return df, valid_tracks


def mfcc_analize(track_path, fft_size=2048, hop_size=512, n_features=20):

    audio, sr = librosa.load(track_path)
    mfcc_data = librosa.feature.mfcc(y=audio, sr=sr, n_fft=fft_size, hop_length=hop_size, n_mfcc=n_features)
    for index, track in enumerate(tracks):
        if track["absolute_path"] == track_path:
            print('añadido mfcc de:', track_path)
            tracks[index]["mfcc"] = mfcc_data[0]


def centroid_analize(track_path, fft_size=2048, hop_size=512):

    audio, sr = librosa.load(track_path)
    centroid_data = librosa.feature.spectral_centroid(y=audio, sr=sr, n_fft=fft_size, hop_length=hop_size)
    for index, track in enumerate(tracks):
        if track["absolute_path"] == track_path:
            print('añadido centroide de:', track_path)
            tracks[index]["centroid"] = centroid_data[0]


tracks = tracks_info(CORPUS_FOLDER_PATH)[0] #aqui estava el problema. Tens que dir-li que de les dos infos que return tracks_info nomes vols la 1.

[centroid_analize(track["absolute_path"]) for track in tracks]
[mfcc_analize(track["absolute_path"]) for track in tracks]


#print(tracks)
[print(track["track_id"], track["centroid"], track["mfcc"]) for track in tracks]
