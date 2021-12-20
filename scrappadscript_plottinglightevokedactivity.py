# %% imports
import os

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

# %% in all light-evoked neuron recordings, find ...
allneuronrecordings_serieslist = [MDJ_mice_neuronrecordings_names,
                                  midbrain_mice_recordings_names,
                                  Thy1_mice_neuronrecordings_names,
                                  RBP_mice_recordings_names]
lightevokeddays_neuronrecordings_names = pd.concat(allneuronrecordings_serieslist)

# I don't have any experiments in mice with optogenetically-labeled things where TTl-on is used for anything besides
# activating the light. So, we can use get_ttlonmeasures to identify neurons that actually had light responses recorded.
lightevokedneurons_list = []
lightevokedAPsneurons_list = []
for neuron in lightevokeddays_neuronrecordings_names:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    if not neuron_data.ttlon_measures.empty:
        lightevokedneurons_list.append(neuron)
        if neuron_data.ttlon_measures.response_maxamp.max() > 40:
            lightevokedAPsneurons_list.append(neuron)

# print(lightevokedneurons_list)
# ['20210411A', '20210411B', '20210411C', '20210411F', '20210413A', '20210413B', '20210426B', '20210426C', '20210426D', '20210426E', '20210426F', '20210110A', '20210110C', '20210110D', '20210110E', '20210110F', '20210110G', '20210113A', '20210113B', '20210113C', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210123C', '20210123D', '20210124A', '20210124B', '20210124C', '20210124D', '20210203A', '20210203B', '20210203C', '20190527A', '20190527C', '20190529A1', '20190529B', '20190529C', '20190529D', '20190529E', '20200630A', '20200630B1', '20200630B2', '20200630C', '20200630D', '20200701A', '20200701B', '20200701D', '20200706B', '20200706D', '20200706E', '20200707B', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20200708G', '20210105A', '20210105B', '20210105C', '20210105D', '20210105E', '20210429A1', '20210429A2', '20210429B', '20200818B', '20200818C', '20201124A', '20201124C', '20201125B', '20201125C', '20201125D', '20201125E', '20201125F']

# print(lightevokedAPsneurons_list)
# ['20210413B', '20210426B', '20210110A', '20210110D', '20210110E', '20210110F', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210124B', '20210124C', '20210124D', '20190527A', '20190527C', '20190529A1', '20190529B', '20190529D', '20200630A', '20200630B2', '20200630C', '20200630D', '20200701A', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20210105B', '20210105D', '20201124C', '20201125B', '20201125C', '20201125D']


# %%
rawdatacleanup_required_list = []
depolevents_notextracted_list = []
has_evokedAPsextracted_list = []
has_spontAPsextracted_list = []

storedresultsfolder_path = path + '\\' + 'myResults'
resultsfiles_list = os.listdir(storedresultsfolder_path)
for neuron in lightevokedneurons_list:
    neuron_resultsfiles = [file for file in resultsfiles_list if neuron in file]
    if not neuron_resultsfiles:
        rawdatacleanup_required_list.append(neuron)
    else:
        neuron_depoleventsfile = [file for file in neuron_resultsfiles if 'depolarizing_events' in file]
        if not neuron_depoleventsfile:
            depolevents_notextracted_list.append(neuron)
        else:
            neuron_depoleventsfile_path = storedresultsfolder_path + '\\' + neuron_depoleventsfile[0]
            neuron_depolevents = pd.read_csv(neuron_depoleventsfile_path, index_col=0)
            spontaps = ((neuron_depolevents.event_label == 'actionpotential') & ~(neuron_depolevents.applied_ttlpulse))
            evokedaps = ((neuron_depolevents.event_label == 'actionpotential') & (neuron_depolevents.applied_ttlpulse))
            if sum(spontaps) > 0:
                has_spontAPsextracted_list.append(neuron)
            if sum(evokedaps) > 0:
                has_evokedAPsextracted_list.append(neuron)



spontandevokedaps_neurons_list = list(set(has_spontAPsextracted_list) & set(has_evokedAPsextracted_list))
# print(spontandevokedaps_neurons_list)
# ['20190527A', '20190529A1', '20190529D', '20200630C', '20200708D', '20200708F', '20201125D', '20210105D', '20210113G', '20210113H', '20210426B']
# none are from MDJ-labeled experiments (some are from midbrain-labeled experiments)
# %% split out by where the optogenetically activated innervation is coming from
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
#20210411F - clear example of evoked fast-events: multiple amp groups, largest ones disappear first with hyperpolarization. Too bad it has terrible baselinev (>-30mV even with huge -DC) and no spont.APs.
#20210413B - oscillating throughout with spont.fast-events, responding to light with APs or fast-things at hyperpolarized potentials
#20210426B - has spont.APs and fast-events, light evokes AP almost every time. Bad baselinev and noisy data.

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
