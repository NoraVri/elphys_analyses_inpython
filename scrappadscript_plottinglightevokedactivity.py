# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# metadata imports
path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

MDJ_mice = ['HUM050', 'HUM051', 'HUM052', 'HUM053', 'HUM054', 'HUM055']
MDJ_mice_condition = experimentdays_metadata.virusinjection_ID.isin(MDJ_mice)
MDJ_mice_experiments_dates = experimentdays_metadata[MDJ_mice_condition].date
MDJ_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(MDJ_mice_experiments_dates)]
MDJ_mice_neuronrecordings_names = MDJ_mice_neuronrecordings.name.dropna()

midbrain_mice = ['HUM042', 'HUM043', 'HUM044', 'HUM045', 'HUM046',]
midbrain_mice_experiments_dates = experimentdays_metadata[experimentdays_metadata.virusinjection_ID.isin(midbrain_mice)].date
midbrain_mice_recordings_names = recordings_metadata[recordings_metadata.date.isin(midbrain_mice_experiments_dates)].name.dropna()

Thy1_mice = ['Thy1', 'thy1']
Thy1_mice_condition = experimentdays_metadata.genetics.isin(Thy1_mice)
Thy1_mice_experiments_dates = experimentdays_metadata[Thy1_mice_condition].date
Thy1_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(Thy1_mice_experiments_dates)]
Thy1_mice_neuronrecordings_names = Thy1_mice_neuronrecordings.name.dropna()

RBP_mice = ['RBP', 'RBP4-cre/Ai32']
RBP_mice_experiments_dates = experimentdays_metadata[experimentdays_metadata.genetics.isin(RBP_mice)].date
RBP_mice_recordings_names = recordings_metadata[recordings_metadata.date.isin(RBP_mice_experiments_dates)].name.dropna()

# %%
RBP_lightevokedAPs_recordings = []
for neuron in RBP_mice_recordings_names:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    if not neuron_data.ttlon_measures.empty:
        if neuron_data.ttlon_measures.response_maxamp.max() > 40:
            RBP_lightevokedAPs_recordings.append(neuron)
            neuron_data.plot_rawdatatraces_ttlaligned()

# recordings of particular interest:

# %%
MDJ_lightevokedAPs_recordings = []
for neuron in MDJ_mice_neuronrecordings_names:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    if not neuron_data.ttlon_measures.empty:
        neuron_data.plot_rawdatatraces_ttlaligned()
        if neuron_data.ttlon_measures.response_maxamp.max() > 40:
            MDJ_lightevokedAPs_recordings.append(neuron)

# recordings of particular interest:
#20210411F - clear example of evoked fast-events: multiple amp groups, largest ones disappear first with hyperpolarization

# %%
midbrain_lightevokedAPs_recordings = []
for neuron in midbrain_mice_recordings_names:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    if not neuron_data.ttlon_measures.empty:
        if neuron_data.ttlon_measures.response_maxamp.max() > 40:
            midbrain_lightevokedAPs_recordings.append(neuron)
            neuron_data.plot_rawdatatraces_ttlaligned()
# recordings of particular interest:

# %%
Thy1_lightevokedAPs_recordings = []
for neuron in Thy1_mice_neuronrecordings_names:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    if not neuron_data.ttlon_measures.empty:
        if neuron_data.ttlon_measures.response_maxamp.max() > 40:
            midbrain_lightevokedAPs_recordings.append(neuron)
            neuron_data.plot_rawdatatraces_ttlaligned()
# recordings of particular interest:
