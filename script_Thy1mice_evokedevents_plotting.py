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

Thy1_mice = ['Thy1', 'thy1']
Thy1_mice_condition = experimentdays_metadata.genetics.isin(Thy1_mice)
Thy1_mice_experiments_dates = experimentdays_metadata[Thy1_mice_condition].date
Thy1_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(Thy1_mice_experiments_dates)]
Thy1_mice_neuronrecordings_names = Thy1_mice_neuronrecordings.name.dropna()


# %%
neuron_data = SingleNeuron('20200701D')
df1, df2 = neuron_data.plot_rawdatatraces_ttlaligned()

# %%
neuron_data2 = SingleNeuron('20190527A')


# %%
for neuron in Thy1_mice_neuronrecordings_names:
    neuron_data = SingleNeuron(neuron)
    neuron_data.plot_rawdatatraces_ttlaligned(baseline_lims=[-90, -30])

