# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import os
import re
import json

from dotenv import load_dotenv
load_dotenv()
rawdata_path = os.environ.get('RAWDATA_PATH')
datafolder_path = rawdata_path + '\\Data_recordedByDeNard'  # in 2024, Vclamp data was all recorded by DeNard
neuron_recordings_list = os.listdir(datafolder_path)  # this works because I manually split recordings from each day into one folder per neuron, based on notes DeNard wrote in .rtf files for each day
# setting up a recordings_metadata table for these recordings:
dates_list = []
for neuron_name in neuron_recordings_list:
    dates_list.append(neuron_name[:6])
neuron_recordings_df = pd.DataFrame({'date':dates_list, 'neuron_name':neuron_recordings_list})






