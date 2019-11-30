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


# ----- constants ------ #

CORPUS_FOLDER_PATH = join(getcwd(),  "sounds")

# --------------------- #


def is_valid_sound(file):
    return isfile(file) and file.lower().endswith(('.wav', '.aiff'))


def create_valid_audio_absolute_paths(tracks_folder_path):
    track_fullpaths = []
    for track_filename in listdir(tracks_folder_path):
        track_absolute_path = join(tracks_folder_path, track_filename)
        if(not is_valid_sound(track_absolute_path)):
            print('invalid format for ', track_filename, ' ,only wav or aiff')
            continue
        track_fullpaths.append(track_absolute_path)
    return track_fullpaths


def mfcc_analize(track_path, fft_size=2048, hop_size=512, n_features=20):
    audio, sr = librosa.load(track_path)
    mfcc_data = librosa.feature.mfcc(y=audio, sr=sr, n_fft=fft_size, hop_length=hop_size, n_mfcc=n_features)
    return mfcc_data



# ----- MAIN ------ #
'''NOTE: tracks_to_path.json, is it really necessary? why not the object id is the fullpath instead of track_id?'''

# 1 - list of valid audio fullpaths
track_fullpaths = create_valid_audio_absolute_paths(CORPUS_FOLDER_PATH)
[print(track) for track in track_fullpaths]

# 2 - iterate over fullpaths, create object where {fullpath: {MFCC: anakysis}}  so we can fullpath[MFCC], or save in npy files
resultat = [mfcc_analize(track_path) for track_path in track_fullpaths]
print(resultat)
print(resultat[0].shape)

'''
TODOS:
 * Define the python interface with other programs (instead of by_frame_id, maybe get_similar_by_X(track, framePosition))
 * Save results of MFFC and other anaylisis(centroid etc) in json or numpy
 * Super-exact function to retrieve correct frame given track and position
 * Think about id: is it better fullpath (harder to share) or filename(harder to access)
 * Think a nice pattern to analyse different features. 
'''
