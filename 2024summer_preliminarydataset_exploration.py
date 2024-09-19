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
datafolder_path = rawdata_path + '\\Data'
allrecordings_list = os.listdir(datafolder_path)

datasetrecordings_list = [recording for recording in allrecordings_list if ('2406' in recording) or ('2407' in recording)]
datasetrecordings_list = [recording for recording in datasetrecordings_list if '0611' not in recording]



# %%
optorecordings_list = []
sulpiriderecordings_list = []
quinpirolerecordings_list = []
basicpropertiesrecordings_list = []

for recording in datasetrecordings_list:
    recordingfiles_path = datafolder_path + '\\' + recording
    recordingfiles_list = os.listdir(recordingfiles_path)
    if sum(['opto' in rec for rec in recordingfiles_list]) > 1:
        optorecordings_list.append(recording)
    if sum(['ulpirid' in rec for rec in recordingfiles_list]) > 1:
        sulpiriderecordings_list.append(recording)
    if sum(['uinpirol' in rec for rec in recordingfiles_list]) > 1:
        quinpirolerecordings_list.append(recording)
    if ((sum(['longPulse' in rec for rec in recordingfiles_list]) > 1) and (sum(['short' in rec for rec in recordingfiles_list]) >= 1)):
        basicpropertiesrecordings_list.append(recording)

sulpiride_probablynicerecordings = list(set(sulpiriderecordings_list) & set(basicpropertiesrecordings_list))
sulpiride_probablynicerecordings.sort()
quinpirole_probablynicerecordings = list(set(quinpirolerecordings_list) & set(basicpropertiesrecordings_list))
quinpirole_probablynicerecordings.sort()

drugsrecordings = sulpiriderecordings_list + quinpirolerecordings_list
nolightresponse_neurons = list(set(basicpropertiesrecordings_list) - set(drugsrecordings))
nolightresponse_neurons.sort()


# %%
for neuron in sulpiride_probablynicerecordings:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    subthresholdresponses_df = neuron_data.ttlon_measures[neuron_data.ttlon_measures.response_maxamp < 30]
    subthresholdresponses_withdrug_df = subthresholdresponses_df[subthresholdresponses_df.file_origin.str.contains('ith')]
    figure, axes = plt.subplots(1, 1, squeeze=True)
    subthresholdresponses_df.plot.scatter('baselinev', 'response_maxamp',
                              ax=axes)
    subthresholdresponses_withdrug_df.plot.scatter('baselinev', 'response_maxamp',
                               c='red',
                               ax=axes)
    figure.legend(['no drug', 'drug'])
    figure.suptitle(neuron_data.name)


# %%
for neuron in nolightresponse_neurons:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=10)
    neuron_data.ttlon_measures.plot.scatter('baselinev', 'response_maxamp')
    # neuron_data.plot_rawdatablocks('longPulses_0001')
    # neuron_data.plot_rawdatablocks('optoStim_100')

# %% for visual comparison: EPSP from opto-evoked synaptic input in IO neuron

neuron_name = '20201125B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_ttlonmeasures_fromrawdata()
neuron_data.ttlon_measures.plot.scatter('baselinev', 'response_maxamp')
