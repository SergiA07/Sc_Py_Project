


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

CORPUS_PATH = "/Users/Sergi/Documents/SuperCollider/Proyectos/Eloi/sons"



# ----------- #


def is_valid_sound(file):
    isValidSound = isfile(file) and file.lower().endswith(('.wav', '.aiff'))
    if(not isValidSound): print('invalid sound format for ', file, 'only wav or aiff')
    return isValidSound



def track_info_creator(track_name, folder_path):
    # Create a dictionary with the metadata that we want to store for each sound clip."""
    track_name = track_name.split("/")
    track_name = track_name[-1]

    track_info = {}
    track_info["track_id"] = track_name
    track_info["absolute_path"] = join(folder_path, track_name)
    return track_info






def tracks_info(sound_files_path):

    # Make a Pandas DataFrame with the metadata of our sound collection and save it
    tracks_paths = [join(sound_files_path, track) for track in listdir(sound_files_path)]


    valid_tracks = [f for f in tracks_paths if is_valid_sound(f)]


    # df =  pd.DataFrame([track_info_creator(tr, sound_files_path) for tr in valid_tracks])
    # df.sort_values('track_id', inplace=True) #sort alphabetically
    # return df, valid_tracks

    tracks_info = [track_info_creator(track, sound_files_path) for track in valid_tracks]
    return tracks_info, valid_tracks


def mfcc_analize(track_path, fft_size=2048, hop_size=512, n_features=20):
    audio, sr = librosa.load(track_path)
    mfcc_data = librosa.feature.mfcc(y=audio, sr=sr, n_fft=fft_size, hop_length=hop_size, n_mfcc=n_features)
    return mfcc_data


tracks = tracks_info(CORPUS_PATH)[0] #aqui estava el problema. Tens que dir-li que de les dos infos que return tracks_info nomes vols la 1.

print(tracks)

print()

resultat = [mfcc_analize(track["absolute_path"]) for track in tracks]

print(resultat)
