# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import singleneuron_plotting_functions as plots

# In this script: analysis of APs as triggered from fast-events.
# Dataset: neurons recorded on days with optogenetic activation of inputs to IO.

# metadata imports
path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

# analyses step0: go to script_rawdata_importing and go over raw data for each neuron in the dataset (N=99).
# analyses step0.1: get list of neurons again, but without those whose total_t_recorded_in_s = 0 (neuron data excluded)

# getting all IO neuron recordings
IOneurons_recordings = (recordings_metadata.anatomical_location == 'inferior_olive') \
                       & (recordings_metadata.total_t_recorded_in_s > 0)
# getting all experiment days that optogenetically activatable inputs were in the slice,
# split out per type of labeled inputs:
virus_toMidbrain_mice = ['HUM042', 'HUM043', 'HUM044', 'HUM045', 'HUM046']
virus_toMDJ_mice = ['HUM050', 'HUM051', 'HUM052', 'HUM053', 'HUM054', 'HUM055']
RBP_mice = ['RBP', 'RBP4-cre/Ai32']
Thy1_mice = ['Thy1', 'thy1']

expdays_virus_toMidbrain = experimentdays_metadata[
    experimentdays_metadata.virusinjection_ID.isin(virus_toMidbrain_mice)].date
expdays_virus_toMDJ = experimentdays_metadata[
    experimentdays_metadata.virusinjection_ID.isin(virus_toMDJ_mice)].date
expdays_RBP = experimentdays_metadata[experimentdays_metadata.genetics.isin(RBP_mice)].date
expdays_Thy1 = experimentdays_metadata[experimentdays_metadata.genetics.isin(Thy1_mice)].date

# getting IO neuron recordings from days that optogenetically activatable inputs were in the slice
# split out per input type
recordings_virus_toMidbrain = recordings_metadata[(IOneurons_recordings
                                                   & recordings_metadata.date.isin(expdays_virus_toMidbrain))]
recordings_virus_toMidbrain['mouse_type'] = 'virus_toMidbrain'
recordings_virus_toMDJ = recordings_metadata[(IOneurons_recordings
                                              & recordings_metadata.date.isin(expdays_virus_toMDJ))]
recordings_virus_toMDJ['mouse_type'] = 'virus_toMDJ'
recordings_RBP = recordings_metadata[(IOneurons_recordings
                                      & recordings_metadata.date.isin(expdays_RBP))]
recordings_RBP['mouse_type'] = 'RBP'
recordings_Thy1 = recordings_metadata[(IOneurons_recordings
                                       & recordings_metadata.date.isin(expdays_Thy1))]
recordings_Thy1['mouse_type'] = 'Thy1'
# all together
expdays_lightactive_all = pd.concat([expdays_virus_toMidbrain, expdays_virus_toMDJ, expdays_RBP, expdays_Thy1])
recordings_dfs_list = [recordings_Thy1, recordings_RBP, recordings_virus_toMDJ, recordings_virus_toMidbrain]
recordings_lightactive_all = pd.concat(recordings_dfs_list)
# Total number of neurons in the dataset: N = 77.

# %% analyses step1: getting APs and depolarizing events for all neurons in the dataset.
# Go to [neuronname]_script_groupingdepolarizingevents to see notes on labeling depolarizing events for each neuron.
# analyses step1.1: determining which neurons have spont. fastevents and/or APs, and light-evoked events and/or APs.
# hasno_depolevents_extracted_list = []
# hasno_lightactivations_list = []
# has_spontAPs_list = []
# has_DCevokedAPs_list = []
# has_fastevents_list = []
# has_neatevents_list = []
# has_lightresponses_list = []
# has_lightevokedAPs_list = []
# I don't have any experiments in mice with optogenetically-labeled things where TTl-on is used for anything besides
# activating the light. So, we can use get_ttlonmeasures to identify neurons that actually had light responses recorded.
# filling in the lists:
# for neuron in recordings_lightactive_all.name:
#     neuron_data = SingleNeuron(neuron)
#     neuron_data.get_ttlonmeasures_fromrawdata()
#     if neuron_data.ttlon_measures.empty:
#         hasno_lightactivations_list.append(neuron)
#
#     if neuron_data.depolarizing_events.empty:
#         hasno_depolevents_extracted_list.append(neuron)
#     elif sum(~(neuron_data.depolarizing_events.event_label.isna())) > 0:
#         spontAPs = ((neuron_data.depolarizing_events.event_label == 'actionpotential')
#                     & ~neuron_data.depolarizing_events.applied_ttlpulse)
#         if sum(spontAPs) > 0:
#             has_spontAPs_list.append(neuron)
#         currentevokedAPs = (neuron_data.depolarizing_events.event_label == 'actionpotential_on_currentpulsechange')
#         if sum(currentevokedAPs) > 0:
#             has_DCevokedAPs_list.append(neuron)
#         fastevents = (neuron_data.depolarizing_events.event_label == 'fastevent')
#         if sum(fastevents) > 0:
#             has_fastevents_list.append(neuron)
#         evokedevents = (neuron_data.depolarizing_events.applied_ttlpulse)
#         if sum(evokedevents) > 0:
#             has_lightresponses_list.append(neuron)
#         lightevoked_aps = (evokedevents & (neuron_data.depolarizing_events.event_label == 'actionpotential'))
#         if sum(lightevoked_aps) > 0:
#             has_lightevokedAPs_list.append(neuron)
#         if 'neat_event' in neuron_data.depolarizing_events.columns:
#             has_neatevents_list.append(neuron)

# %% neuron recordings lists
# list of all neuron recordings in the dataset:
dataset_neuronrecordings_list = [
    '20190527A',  # checked APs; checked fastevents; checked neatevents
    '20190527B',  # checked APs; checked fastevents; checked neatevents
    '20190527C',  # no APs (!); checked fastevents; no neatevents  - !light may be evoking highly degenerate APs; APs cannot be evoked through DC
    '20190529A1', # checked APs; checked fastevents; checked neatevents
    '20190529A2', # checked APs; checked fastevents; no neatevents
    '20190529B',  # checked APs; no fastevents; checked neatevents (APs are lightevoked)
    '20190529C',  # no APs; checked fastevents; no neatevents
    '20190529D',  # checked APs; checked fastevents; no neatevents
    '20190529E',  # checked APs; no fastevents; no neatevents (APs are DC-evoked)
    '20200630A',  # checked APs; no fastevents; no neatevents (APs are light-evoked)
    '20200630B1', # checked APs; no fastevents; no neatevents (the single spont.AP may be from pre-potential)
    '20200630B2', # checked APs; no fastevents; no neatevents (neat recording but no events; APs are light- or DC-evoked)
    '20200630C',  # checked APs; checked fastevents; checked neatevents
    '20200630D',  # checked APs; checked fastevents; checked neatevents (!)  - !about half of fastevents have an AHP that looks like it comes from the network - not sure if averaging is fair, even though they do all look 'neat'
    '20200701A',  # checked APs; checked fastevents; checked neatevents
    '20200701B',  # no APs; checked fastevents; no neatevents
    '20200701D',  # no APs; no fastevents; no neatevents
    '20200706A',  # checked APs; no fastevents; no neatevents (spont.APs all from pre-potential; resting baselineV >-40mV throughout)
    '20200706B',  #! checked APs; checked fastevents; checked neatevents  - !may need to exclude non-neat data (including light response)
    '20200706D',  # no APs; no fastevents; no neatevents
    '20200706E',  # checked APs; checked fastevents; not sure about neatevents !1mM Ca in slicing solution that day; ambiguous effect on recordings
    '20200707E',  # checked APs; no fastevents; no neatevents (APs are light- or DC-evoked)
    '20200708A',  # checked APs; checked fastevents; no neatevents
    '20200708B',  # checked APs; checked fastevents; checked neatevents
    '20200708C',  # checked APs; no fastevents; no neatevents (one each of spont. and light-evoked AP, both without pre-potential)
    '20200708D',  # checked APs; checked fastevents; checked neatevents
    '20200708E',  # checked APs; checked fastevents; checked neatevents (just 2 min. of recording but what there is of it is very neat and has spont.activity)
    '20200708F',  # checked APs; checked fastevents; checked neatevents
    '20200708G',  # no APs; no fastevents; no neatevents
    '20200818B',  # checked APs; checked fastevents; checked neatevents
    '20200818C',  # checked APs; no fastevents; no neatevents (APs are spont and both have pre-potential)
    '20201124C',  # checked APs; checked fastevents; no neatevents
    '20201125B',  # checked APs; checked fastevents; checked neatevents
    '20201125C',  # checked APs; checked fastevents; checked neatevents
    '20201125D',  # checked APs; checked fastevents; checked neatevents
    '20201125E',  # checked APs; checked fastevents; no neatevents
    '20201125F', # undecided about APs and fastevents
    '20210105A',  # checked APs; checked fastevents; no neatevents
    '20210105B',  # checked APs; checked fastevents; no neatevents
    '20210105C',  # checked APs; no fastevents; no neatevents (APs are DC-evoked)
    '20210105D',  # checked APs; checked fastevents; no neatevents
    '20210105E',  # checked APs; no fastevents; no neatevents (APs are DC-evoked)
    '20210110A',  # checked APs; checked fastevents; checked neatevents
    '20210110B',  # checked APs; no fastevents; no neatevents (APs are DC-evoked or happen because neuron is depolarizing while dying slowly)
    '20210110C',  # checked APs; no fastevents; no neatevents (APs are DC-evoked)
    '20210110D',  # checked APs; checked fastevents; checked neatevents
    '20210110E',  # checked APs; checked fastevents; checked neatevents
    '20210110F',  # checked APs; checked fastevents; no neatevents
    '20210110G',  # checked APs; checked fastevents; checked neatevents (only three spont.subthreshold events; APs only current-evoked)
    '20210113A', # checked APs; undecided about fastevents
    '20210113B',  # checked APs; no fastevents; no neatevents (APs are DC-evoked)
    '20210113C',  # checked APs; checked fastevents; checked neatevents
    '20210113D',  # checked APs; checked fastevents; checked neatevents
    '20210113E',  # checked APs; no fastevents; no neatevents (APs from pre-potential w/o fastevents alone present)
    '20210113F',  # checked APs; no fastevents; no neatevents (APs are light-evoked)
    '20210113G',  # checked APs; checked fastevents; checked neatevents
    '20210113H',  # checked APs; checked fastevents; checked neatevents (very nice example for evoking 2 different amplitude fastevents (and an AP from the largest one))
    '20210123B',  # checked APs; checked fastevents; no neatevents
    '20210123D',  # checked APs; checked fastevents; checked neatevents
    '20210124A',  # checked APs; checked fastevents; checked neatevents
    '20210124B',  # checked APs; checked fastevents; checked neatevents
    '20210124C',  # checked APs; checked fastevents; no neatevents
    '20210124D',  # checked APs; no fastevents; no neatevents (the one spont.AP occurs under leaky conditions).
    '20210203A',  # checked APs; no fastevents; no neatevents (the one spont.AP doesn't seem to have a fastevent-prepotential)
    '20210203B',  # checked APs; checked fastevents; checked neatevents
    '20210203C',  # checked APs; checked fastevents; checked neatevents
    '20210411A', # no APs; undecided about fastevents; no neatevents
    '20210411B',  # checked APs; no fastevents; no neatevents (APs are DC-evoked)
    '20210411C',  # checked APs; checked fastevents; no neatevents
    '20210411F',  # no APs; checked fastevents; no neatevents
    '20210413A',  # checked AP; checked fastevent; no neatevents
    '20210413B',  # checked APs; checked fastevents; no neatevents
    '20210426B',  # checked APs; checked fastevents; no neatevents
    '20210426C',  # checked APs; checked fastevents; no neatevents
    '20210426D',  # checked APs; checked fastevents; checked neatevents (spont.APs are very weirdly degenerate, as though no Na-component [while fastevents persist...])
    '20210426E',  # checked APs; no fastevents; no neatevents (APs are DC-evoked)
    '20210429B'   # no APs; no fastevents; no neatevents
]

# lists as of Tuesday 20220511
hasno_depolevents_extracted_list = []

hasno_lightactivations_list = ['20190527B', '20190529A2', '20200706A', '20200708A', '20200708E', '20210110B', '20210113E', '20210411C']

has_spontAPs_list = ['20190527A', '20190527B', '20190529A1', '20190529D', '20200630B1', '20200630C', '20200701A', '20200706A', '20200706B', '20200706E', '20200708A', '20200708B', '20200708C', '20200708D', '20200708E', '20200708F', '20200818C', '20201124C', '20201125B', '20201125D', '20201125F', '20210105A', '20210105B', '20210105D', '20210110A', '20210113G', '20210113H', '20210124A', '20210413B', '20210426D']

has_fastevents_list = ['20190527A', '20190527B', '20190527C', '20190529A1', '20190529A2', '20190529C', '20190529D', '20200630C', '20200630D', '20200701A', '20200701B', '20200706B', '20200706E', '20200708A', '20200708B', '20200708D', '20200708E', '20200708F', '20200818B', '20201124C', '20201125B', '20201125C', '20201125D', '20201125E', '20210105A', '20210105B', '20210105D', '20210110A', '20210110D', '20210110E', '20210110G', '20210113C', '20210113D', '20210113G', '20210113H', '20210123B', '20210123D', '20210124A', '20210124B', '20210124C', '20210203B', '20210203C', '20210411C', '20210411F', '20210413A', '20210413B', '20210426B', '20210426C', '20210426D']

has_neatevents_list = ['20190527A', '20190527B', '20190529A1', '20190529B', '20200630C', '20200630D', '20200701A', '20200706B', '20200708B', '20200708D', '20200708E', '20200708F', '20200818B', '20201125B', '20201125C', '20201125D', '20210110A', '20210110D', '20210110E', '20210110G', '20210113C', '20210113D', '20210113G', '20210113H', '20210123D', '20210124A', '20210124B', '20210203B', '20210203C', '20210426D']

has_lightresponses_list = ['20190527A', '20190527C', '20190529A1', '20190529B', '20190529C', '20190529D', '20190529E', '20200630A', '20200630B1', '20200630B2', '20200630C', '20200630D', '20200701A', '20200701B', '20200706B', '20200706D', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20200708G', '20200818B', '20201124C', '20201125B', '20201125C', '20201125D', '20201125E', '20201125F', '20210105A', '20210105B', '20210105C', '20210105D', '20210110A', '20210110C', '20210110D', '20210110E', '20210110F', '20210113A', '20210113B', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210123D', '20210124A', '20210124B', '20210124C', '20210124D', '20210411B', '20210411F', '20210413A', '20210413B', '20210426B', '20210426C', '20210426D', '20210426E', '20210429B']

has_lightevokedAPs_list = ['20190527A', '20190529A1', '20190529B', '20190529D', '20200630A', '20200630B2', '20200630C', '20200630D', '20200701A', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20201124C', '20201125B', '20201125C', '20201125D', '20201125E', '20210105B', '20210105D', '20210110A', '20210110D', '20210110E', '20210110F', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210124B', '20210124C', '20210124D', '20210413B', '20210426B']

has_DCevokedAPs_list = ['20190527A', '20190527B', '20190529A1', '20190529A2', '20190529B', '20190529E', '20200630B1', '20200630B2', '20200630C', '20200707E', '20200708F', '20200818B', '20200818C', '20201124C', '20201125B', '20201125C', '20210105C', '20210105E', '20210110A', '20210110B', '20210110C', '20210110E', '20210110F', '20210110G', '20210113A', '20210113B', '20210113C', '20210113D', '20210113G', '20210113H', '20210123B', '20210123D', '20210124A', '20210124B', '20210124C', '20210124D', '20210203A', '20210203B', '20210203C', '20210411B', '20210413A', '20210426B', '20210426C', '20210426D', '20210426E']


# %% summary table: types of events in all neurons
# data table listing all neurons in the dataset by ID; light-activation preparation; presence of light applications; light responses (subthreshold and AP); fastevents; neatevents.

# %% analyses step: getting AP prepotential amplitudes (for dataset neurons that have at least 10 APs labeled)
# results_path = path + '\\myResults'
# resultsfiles_all = os.listdir(results_path)
# resultsfiles_depolarizingevents = [filename for filename in resultsfiles_all if 'depolarizing_events' in filename]
# for filename in resultsfiles_depolarizingevents:
#     filepath = results_path + '\\' + filename
#     neuron_depolarizingevents = pd.read_csv(filepath)
#     if sum((neuron_depolarizingevents.event_label == 'actionpotential')) >= 10:
#         neuron_name = re.split('_d', filename)[0]
#         if neuron_name in dataset_neuronrecordings_list:
#             neuron_data = SingleNeuron(neuron_name)
#             neuron_data.get_ap_prepotentials((neuron_data.depolarizing_events.event_label == 'actionpotential'))
#             neuron_data.write_results()

# %% data table: APs from prepotentials (neurons with 10 or more labeled APs (spont.or evoked))
results_path = path + '\\myResults'
resultsfiles_all = os.listdir(results_path)
resultsfiles_depolarizingevents = [filename for filename in resultsfiles_all if 'depolarizing_events' in filename]
n_aps_dict = {'neuron_name': [],
              'n_spontAPs': [],
              'n_spontAPs_withprepotential': [],
              'n_neatspontAPs': [],
              'n_neatspontAPs_withprepotential': [],
              'n_evokedAPs': [],
              'n_evokedAPs_withprepotential': [],
              'n_neatevokedAPs': [],
              'n_neatevokedAPs_withprepotential': [],
              }
for filename in resultsfiles_depolarizingevents:
    filepath = results_path + '\\' + filename
    neuron_depolarizingevents = pd.read_csv(filepath)
    aps = neuron_depolarizingevents.event_label == 'actionpotential'
    if ('ap_prepotential_amp' in neuron_depolarizingevents.columns):
        neuron_name = re.split('_d', filename)[0]
        spontaps = aps & ~(neuron_depolarizingevents.applied_ttlpulse)
        evokedaps = aps & neuron_depolarizingevents.applied_ttlpulse
        aps_withprepotential = aps & ~neuron_depolarizingevents.ap_prepotential_amp.isna()
        spontaps_withprepotential = spontaps & aps_withprepotential
        evokedaps_withprepotential = evokedaps & aps_withprepotential
        if 'neat_event' in neuron_depolarizingevents.columns:
            neat_aps = aps & neuron_depolarizingevents.neat_event
            n_neatspontaps = sum(spontaps & neat_aps)
            n_neatspontaps_withprepotential = sum(spontaps & neat_aps & aps_withprepotential)
            n_neatevokedaps = sum(evokedaps & neat_aps)
            n_neatevokedaps_withprepotential = sum(evokedaps & neat_aps & aps_withprepotential)
        else:
            n_neatspontaps = 0
            n_neatspontaps_withprepotential = 0
            n_neatevokedaps = 0
            n_neatevokedaps_withprepotential = 0
        n_aps_dict['neuron_name'].append(neuron_name)
        n_aps_dict['n_spontAPs'].append(sum(spontaps))
        n_aps_dict['n_spontAPs_withprepotential'].append(sum(spontaps_withprepotential))
        n_aps_dict['n_neatspontAPs'].append(n_neatspontaps)
        n_aps_dict['n_neatspontAPs_withprepotential'].append(n_neatspontaps_withprepotential)
        n_aps_dict['n_evokedAPs'].append(sum(evokedaps))
        n_aps_dict['n_evokedAPs_withprepotential'].append(sum(evokedaps_withprepotential))
        n_aps_dict['n_neatevokedAPs'].append(n_neatevokedaps)
        n_aps_dict['n_neatevokedAPs_withprepotential'].append(n_neatevokedaps_withprepotential)
n_aps_df = pd.DataFrame(n_aps_dict)
# cross-referencing with recordings_lightactive_all to get mouse types for each neuron
cellnames_mousetypes_df_lightactive = recordings_lightactive_all.filter(['name', 'mouse_type'], axis=1)
cellnames_mousetypes_df_renamed = cellnames_mousetypes_df_lightactive.rename(columns={'name': 'neuron_name'})
n_aps_df = n_aps_df.merge(cellnames_mousetypes_df_renamed)  # for each entry in the neuron_name column in n_aps_df that exists also in cellnames_mousetypes_df_renamed neuron_name column, mouse-type data will be merged into n_aps_df.
# %%
# PLOTS: histograms of %APs from prepotentials in these neurons, colored by mouse type (RBP/Thy1/injected):
# spont.APs, for all neurons that have at least one neat spont.AP:
n_spontaps_df = n_aps_df[(n_aps_df.n_neatspontAPs > 0)]
# getting %spontAPs from prepotential
n_spontaps_df['neatspont_percentwithprepotential'] = n_spontaps_df.apply(lambda row: ((row.n_neatspontAPs_withprepotential / row.n_neatspontAPs) * 100), axis=1)
n_spontaps_df.hist(column='neatspont_percentwithprepotential',
                   by='mouse_type',
                   sharex=True, sharey=True,
                   bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])

# evokedAPs, for all neurons that have at least one neat evokedAP:
n_evokedaps_df = n_aps_df[(n_aps_df.n_neatevokedAPs > 0)]
# getting %evokedAPs from prepotential
n_evokedaps_df['neatevoked_percentwithprepotential'] = n_evokedaps_df.apply(lambda row: ((row.n_neatevokedAPs_withprepotential / row.n_neatevokedAPs) * 100), axis=1)
n_evokedaps_df.hist(column='neatevoked_percentwithprepotential',
                   by='mouse_type',
                   sharex=True, sharey=True,
                   bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])

# %% plotting prepotential amplitudes for neurons with 10 or more neat APs
results_path = path + '\\myResults'
resultsfiles_all = os.listdir(results_path)
resultsfiles_depolarizingevents = [filename for filename in resultsfiles_all if 'depolarizing_events' in filename]
i = 0
sum_i = 0
j = 0
sum_j = 0
figure1, axis1 = plt.subplots(1,1,squeeze=True)
spontaps_neurons_list = []
figure2, axis2 = plt.subplots(1,1,squeeze=True)
neatspontaps_neurons_list = []
for filename in resultsfiles_depolarizingevents:
    filepath = results_path + '\\' + filename
    neuron_depolarizingevents = pd.read_csv(filepath)
    if sum((neuron_depolarizingevents.event_label == 'actionpotential')) >= 10:
        neuron_name = re.split('_d', filename)[0]
        if neuron_name in dataset_neuronrecordings_list:
            i += 1
            spontaps_neurons_list.append(neuron_name)
            spont_aps = (neuron_depolarizingevents.event_label == 'actionpotential') \
                             & (~neuron_depolarizingevents.applied_ttlpulse)
            ap_prepotentials_amps = neuron_depolarizingevents.ap_prepotential_amp[spont_aps].dropna()
            jitter = np.random.uniform(-0.2, 0.2, size=len(ap_prepotentials_amps))
            scatter_is = np.ones([len(ap_prepotentials_amps)]) * i + jitter
            sum_i += len(ap_prepotentials_amps)
            axis1.scatter(scatter_is, ap_prepotentials_amps)
            axis1.set_title('all spont APs')
            axis1.set_xlabel('neuron #')
            axis1.set_ylabel('AP prepotential amplitude')

            if 'neat_event' in neuron_depolarizingevents.columns:
                neat_spont_aps = (neuron_depolarizingevents.event_label == 'actionpotential') \
                                 & (~neuron_depolarizingevents.applied_ttlpulse) \
                                 & (neuron_depolarizingevents.neat_event)
                j += 1
                neatspontaps_neurons_list.append(neuron_name)
                prepotentials_amps = neuron_depolarizingevents.ap_prepotential_amp[neat_spont_aps]
                jitter = np.random.uniform(-0.2, 0.2, size=len(prepotentials_amps))
                scatter_is = np.ones([len(prepotentials_amps)]) * j + jitter
                sum_j += len(prepotentials_amps)
                axis2.scatter(scatter_is, prepotentials_amps)
                axis2.set_title('neat spont. APs only')
                axis2.set_xlabel('neuron #')
                axis2.set_ylabel('AP prepotential amplitude')


# %% plots: N aps vs. N aps from prepotential, separately for spont. and evoked
figure1, axes1 = plt.subplots(1, 1, squeeze=True)
n_aps_df.plot.scatter(x='n_spontAPs', y='n_spontAPs_withprepotential',
                      ax=axes1, label='all spont APs', color='r')
n_aps_df.plot.scatter(x='n_neatspontAPs', y='n_neatspontAPs_withprepotential',
                      ax=axes1, label='neat spont APs', color='b')
lims1 = [np.min([axes1.get_xlim(), axes1.get_ylim()]), np.max([axes1.get_xlim(), axes1.get_ylim()])]
axes1.plot(lims1, lims1)  # line: x=y
axes1.plot(lims1, [lim/2 for lim in lims1], '--')  # line: x=y/2
axes1.set_ylim([-5, 150])
axes1.set_xlim([-5, 450])
plt.suptitle('all spontAPs (in neurons that have at least 10 APs recorded)')
axes1.legend()
# re-setting axes limits: neat APs only
axes1.set_ylim([0, 110])
axes1.set_xlim([0, 200])

figure2, axes2 = plt.subplots(1, 1, squeeze=True)
n_aps_df.plot.scatter(x='n_evokedAPs', y='n_evokedAPs_withprepotential',
                      ax=axes2, label='all evoked APs', color='r')
n_aps_df.plot.scatter(x='n_neatevokedAPs', y='n_neatevokedAPs_withprepotential',
                      ax=axes2, label='neat evoked APs', color='b')
lims2 = [np.min([axes2.get_xlim(), axes2.get_ylim()]), np.max([axes2.get_xlim(), axes2.get_ylim()])]
axes2.plot(lims2, lims2)  # line: x=y
axes2.plot(lims2, [lim/2 for lim in lims2], '--')  # line: x=y/2
axes2.set_ylim([-5, 150])
axes2.set_xlim([-5, 450])
plt.suptitle('all evokedAPs (in neurons that have at least 10 APs recorded)')
axes2.legend()
# re-setting axes limits: neat APs only
axes2.set_ylim([0, 20])
axes2.set_xlim([0, 40])

# plot: % APs from prepotential, spont. vs evoked
percentwithprepotential_spont = n_aps_df.n_spontAPs_withprepotential / n_aps_df.n_spontAPs
percentwithprepotential_spont.name = 'percentwithprepotential_spont'
n_aps_df = n_aps_df.join(percentwithprepotential_spont)
percentwithprepotential_spont_neat = n_aps_df.n_neatspontAPs_withprepotential / n_aps_df.n_neatspontAPs
percentwithprepotential_spont_neat.name = 'percentwithprepotential_spont_neat'
n_aps_df =n_aps_df.join(percentwithprepotential_spont_neat)
percentwithprepotential_evoked = n_aps_df.n_evokedAPs_withprepotential / n_aps_df.n_evokedAPs
percentwithprepotential_evoked.name = 'percentwithprepotential_evoked'
n_aps_df = n_aps_df.join(percentwithprepotential_evoked)
percentwithprepotential_evoked_neat = n_aps_df.n_neatevokedAPs_withprepotential / n_aps_df.n_neatevokedAPs
percentwithprepotential_evoked_neat.name = 'percentwithprepotential_evoked_neat'
n_aps_df = n_aps_df.join(percentwithprepotential_evoked_neat)

figure3, axes3 = plt.subplots(1, 1, squeeze=True)
n_aps_df.plot.scatter(x='percentwithprepotential_spont', y='percentwithprepotential_evoked',
                      ax=axes3, label='all APs', color='r')
n_aps_df.plot.scatter(x='percentwithprepotential_spont_neat', y='percentwithprepotential_evoked_neat',
                      ax=axes3, label='neat APs', color='b')
axes3.legend()
axes3.set_xlim([0, 1])
axes3.set_ylim([0, 1])

# plots: N APs against % from prepotential, plotted for spont and for evoked
figure4, axes4 = plt.subplots(1, 1, squeeze=True)
n_aps_df.plot.scatter(x='n_spontAPs', y='percentwithprepotential_spont',
                      ax=axes4, label='spont APs', color='b')
n_aps_df.plot.scatter(x='n_evokedAPs', y='percentwithprepotential_evoked',
                      ax=axes4, label='evoked APs', color='r')
for neuron in n_aps_df.iterrows():
    axes4.plot([neuron[1].n_spontAPs, neuron[1].n_evokedAPs],
               [neuron[1].percentwithprepotential_spont, neuron[1].percentwithprepotential_evoked])

figure5, axes5 = plt.subplots(2, 1, squeeze=True, sharex='all')
n_aps_df['percentwithprepotential_spont'].plot.hist(bins=30, ax=axes5[0])
axes5[0].set_title('portion of spont APs from prepotential')
axes5[0].set_xlim([0, 1])
axes5[0].set_ylim([0, 6])
n_aps_df['percentwithprepotential_evoked'].plot.hist(bins=30, ax=axes5[1])
axes5[1].set_title('portion of evoked APs from prepotential')
axes5[1].set_xlim([0, 1])
axes5[1].set_ylim([0, 6])
# %%
# Figure1 panel: AP prepotential amps as a function of baselineV, for neurons with 5> neat APs

# Figure1 panel: N APs from prepotential/not from prepotential (all APs and neat APs, for neurons with 10> APs)

# color_lims = [0, len(has_spontAPs_list) - 1]
# colormap, cmnormalizer = plots.get_colors_forlineplots([], color_lims)

for idx, neuron in enumerate(has_spontAPs_list):
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ap_prepotentials((neuron_data.depolarizing_events.event_label == 'actionpotential'))
    des_df = neuron_data.depolarizing_events
    aps = des_df.event_label == 'actionpotential'
    spont_events = ~des_df.applied_ttlpulse
    aps_withprepotential = ~des_df.ap_prepotential_amp.isna()
    spont_aps_df = des_df[(aps & spont_events)]
    if 'neat_event' in des_df.columns:
        figure, axes = plt.subplots(1, 2, squeeze=True, sharex='row', sharey='row')
        figure.suptitle(neuron_data.name)
        axes[0].set_title('neat APs')
        neat_events = des_df.neat_event
        neatspontaps_df = des_df[(aps & spont_events & neat_events)]
        neatspontaps_df.plot.scatter(x='baselinev',
                                     y='ap_prepotential_amp',
                                     # color=colormap(cmnormalizer(idx)),
                                     # label=neuron_data.name,
                                     ax=axes[0])
        axes[1].set_title('all APs')
        spont_aps_df.plot.scatter(x='baselinev',
                                  y='ap_prepotential_amp',
                                  ax=axes[1])
    else:
        figure, axes = plt.subplots(1, 1, squeeze=True)
        figure.suptitle(neuron_data.name)
        axes.set_title('all APs')
        spont_aps_df.plot.scatter(x='baselinev',
                                  y='ap_prepotential_amp',
                                  # color=colormap(cmnormalizer(idx)),
                                  # label=neuron_data.name,
                                  ax=axes)

# %% one figure for all neurons with neat fast-events: neat fast-events normalized and averaged
from singleneuron_analyses_functions import get_events_average
figure1, axes1 = plt.subplots(1, 2)
figure2, axes2 = plt.subplots(1, 2)
neuron_list = has_fastevents_list
colormap = mpl.cm.plasma
cmnormalizer = mpl.colors.Normalize(0, len(neuron_list))
for i, neuron in enumerate(neuron_list):
    neuron_data = SingleNeuron(neuron)
    neuron_depolarizingevents = neuron_data.depolarizing_events
    if 'neat_event' in neuron_data.depolarizing_events.keys():
        neat_fastevents = ((neuron_depolarizingevents.event_label == 'fastevent') & (neuron_depolarizingevents.neat_event))
        n_events = sum(neat_fastevents)
        normalized_neatfastevents_avg, \
        normalized_neatfastevents_std, \
        time_axis = get_events_average(neuron_data.blocks,
                                       neuron_data.depolarizing_events,
                                       neuron_data.rawdata_readingnotes['getdepolarizingevents_settings'],
                                       neat_fastevents,
                                       timealignto_measure='rt20_start_idx',
                                       prealignpoint_window_inms=3,
                                       plotwindow_inms=20,
                                       do_normalizing=True)
        linecolor = colormap(cmnormalizer(i))
        axes1[0].plot(time_axis, normalized_neatfastevents_avg, linewidth=2.5, color=linecolor)
        axes1[0].plot(time_axis, (normalized_neatfastevents_avg - normalized_neatfastevents_std), '--', color=linecolor)
        axes1[0].plot(time_axis, (normalized_neatfastevents_avg + normalized_neatfastevents_std), '--', color=linecolor)
        axes1[0].set_xlabel('time (ms)')
        diff_events_avg = np.diff(normalized_neatfastevents_avg)
        axes1[1].plot(normalized_neatfastevents_avg[:-1:], diff_events_avg, color=linecolor, label=(neuron_data.name + ' N=' + str(n_events) + ' events'))

    # figure2: fastevents within baselinerange
        lower_lim = -55
        upper_lim = -45
        baselinerange_neat_fastevents = (neat_fastevents
                                         & (neuron_depolarizingevents.baselinev > lower_lim)
                                         & (neuron_depolarizingevents.baselinev < upper_lim))
        n_baselinerange_events = sum(baselinerange_neat_fastevents)
        if n_baselinerange_events > 0:
            normalized_neatfastevents_avg, \
            normalized_neatfastevents_std, \
            time_axis = get_events_average(neuron_data.blocks,
                                           neuron_data.depolarizing_events,
                                           neuron_data.rawdata_readingnotes['getdepolarizingevents_settings'],
                                           baselinerange_neat_fastevents,
                                           timealignto_measure='rt20_start_idx',
                                           prealignpoint_window_inms=3,
                                           plotwindow_inms=20,
                                           do_normalizing=True)
            linecolor = colormap(cmnormalizer(i))
            axes2[0].plot(time_axis, normalized_neatfastevents_avg, linewidth=2.5, color=linecolor)
            axes2[0].plot(time_axis, (normalized_neatfastevents_avg - normalized_neatfastevents_std), '--',
                          color=linecolor)
            axes2[0].plot(time_axis, (normalized_neatfastevents_avg + normalized_neatfastevents_std), '--',
                          color=linecolor)
            axes2[0].set_xlabel('time (ms)')
            diff_events_avg = np.diff(normalized_neatfastevents_avg)
            axes2[1].plot(normalized_neatfastevents_avg[:-1:], diff_events_avg, color=linecolor,
                          label=(neuron_data.name + ' N=' + str(n_baselinerange_events) + ' events'))

    axes1[1].set_xlabel('V')
    axes1[1].set_ylabel('dV/dt')
    axes1[1].legend(loc='upper left')
    axes2[1].set_xlabel('V')
    axes2[1].set_ylabel('dV/dt')
    axes2[1].legend(loc='upper left')
# %% figure: APs normalized and averaged (see if waveform is identical like for fastevents)
from singleneuron_analyses_functions import get_events_average
figure1, axes1 = plt.subplots(1, 2)
# figure2, axes2 = plt.subplots(1, 2)
neuron_list = has_spontAPs_list
colormap = mpl.cm.plasma
cmnormalizer = mpl.colors.Normalize(0, len(neuron_list))
for i, neuron in enumerate(neuron_list):
    neuron_data = SingleNeuron(neuron)
    neuron_depolarizingevents = neuron_data.depolarizing_events
    if 'neat_event' in neuron_data.depolarizing_events.keys():
        neat_spont_aps = ((neuron_depolarizingevents.event_label == 'actionpotential')
                          & (~neuron_depolarizingevents.applied_ttlpulse)
                          & (neuron_depolarizingevents.neat_event))
        n_events = sum(neat_spont_aps)
        normalized_neatevents_avg, \
        normalized_neatevents_std, \
        time_axis = get_events_average(neuron_data.blocks,
                                       neuron_data.depolarizing_events,
                                       neuron_data.rawdata_readingnotes['getdepolarizingevents_settings'],
                                       neat_spont_aps,
                                       timealignto_measure='rt20_start_idx',
                                       prealignpoint_window_inms=4,
                                       plotwindow_inms=15,
                                       do_normalizing=True)
        linecolor = colormap(cmnormalizer(i))
        axes1[0].plot(time_axis, normalized_neatevents_avg, linewidth=2.5, color=linecolor)
        axes1[0].plot(time_axis, (normalized_neatevents_avg - normalized_neatevents_std), '--', color=linecolor)
        axes1[0].plot(time_axis, (normalized_neatevents_avg + normalized_neatevents_std), '--', color=linecolor)
        axes1[0].set_xlabel('time (ms)')
        diff_events_avg = np.diff(normalized_neatevents_avg)
        axes1[1].plot(normalized_neatevents_avg[:-1:], diff_events_avg, color=linecolor, label=(neuron_data.name + ' N=' + str(n_events) + ' events'))
    axes1[1].set_xlabel('V')
    axes1[1].set_ylabel('dV/dt')
    axes1[1].legend(loc='upper left')
    axes2[1].set_xlabel('V')
    axes2[1].set_ylabel('dV/dt')
    axes2[1].legend(loc='upper left')

# %% analyses step2: seeing APs
# also, get and save recordingblocks_index and ttl_measures
# focusing first on neurons recorded in Thy1 mouse
# while writing text: focusing first on neurons that have neat-events and spont.APs
thy1mouse_neurons = list(recordings_Thy1.name)
has_neatspontAPs = list(set(has_spontAPs_list) & set(has_neatevents_list))
neatspontAPs_and_lightevokedAPs_thy1 = list(set(has_neatspontAPs) & set(has_lightevokedAPs_list) & set(thy1mouse_neurons))
has_neatfastevents_list = list(set(has_fastevents_list) & set(has_neatevents_list))

rbpmouse_neurons = list(recordings_RBP.name)
rbp_spontandlightevoked_aps = list(set(has_spontAPs_list) & set(has_lightevokedAPs_list) & set(rbpmouse_neurons))

neuron_list = has_neatspontAPs #has_lightevokedAPs_list  #thy1mouse_neurons
total_n_neatspontaps = 0
for neuron in neuron_list:
    neuron_data = SingleNeuron(neuron)
    # neuron_data.get_recordingblocks_index()
    # neuron_data.plot_rawdatatraces_ttlaligned()
    # neuron_data.write_results()
    if sum(~neuron_data.depolarizing_events.event_label.isna()) > 0:
        des_df = neuron_data.depolarizing_events
        spont_aps = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
        # neuron_data.plot_depolevents(spont_aps,
        #                              colorby_measure='baselinev',
        #                              prealignpoint_window_inms=10,
        #                              plt_title=' spont.APs')
        neat_spontaps = (spont_aps & (des_df.neat_event))
        neuron_data.plot_depolevents(neat_spontaps,
                                     colorby_measure='baselinev',
                                     prealignpoint_window_inms=10,
                                     plotwindow_inms=16,
                                     plot_ddvdt=True,
                                     plt_title=' neat spont.APs')
        # total_n_neatspontaps += sum(neat_spontaps)
        # lightevoked_aps = (des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse)
        # neuron_data.plot_depolevents(lightevoked_aps,
        #                              colorby_measure='applied_current',
        #                              prealignpoint_window_inms=10,
        #                              plt_title=' light-evoked APs')
        # currentevoked_aps = (des_df.event_label == 'actionpotential_on_currentpulsechange')
        # if sum(currentevoked_aps) > 0:
        #     neuron_data.plot_depolevents(currentevoked_aps,
        #                                  prealignpoint_window_inms=10,
        #                                  colorby_measure='baselinev',
        #                                  plt_title=' DC-evoked APs')
# %% seeing fastevents
for neuron in has_fastevents_list:
    neuron_data = SingleNeuron(neuron)
    if sum(~neuron_data.depolarizing_events.event_label.isna()) > 0:
        des_df = neuron_data.depolarizing_events
        spont_aps = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
        fastevents = (des_df.event_label == 'fastevent')
        if 'neat_event' in des_df.columns:
            neatevents = des_df.neat_event
            neatspontaps = spont_aps & neatevents
            neatfastevents = neatevents & fastevents
            neuron_data.plot_depolevents((neatspontaps | neatfastevents),
                                         colorby_measure='baselinev',
                                         prealignpoint_window_inms=10,
                                         plt_title=' neat spont.events')
        else:
            neuron_data.plot_depolevents((spont_aps | fastevents),
                                         colorby_measure='baselinev',
                                         prealignpoint_window_inms=10,
                                         plt_title=' spont.events')




# %% scatter of ttlresponse measures, per neuron
has_lightapplied_inbaselineVrange_list = []  # definition: lowest baselineV < -60mV, range at least 20mV
results_path = path + '\\myResults'
resultsfiles_all = os.listdir(results_path)
resultsfiles_ttl = [filename for filename in resultsfiles_all if 'ttl' in filename]
for filename in resultsfiles_ttl:
    cell_name = re.split('_', filename)[0]
    filepath = results_path + '\\' + filename
    neuron_ttlonmeasures = pd.read_csv(filepath)
    subthreshold_responses = neuron_ttlonmeasures[neuron_ttlonmeasures.response_maxamp < 40]
    if ((subthreshold_responses.baselinev.min() <= -60)
            & ((subthreshold_responses.baselinev.min() - subthreshold_responses.baselinev.max()) <= -20)):
        # subthreshold_responses.plot.scatter('baselinev', 'response_maxdvdt')
        # plt.title(cell_name)
        has_lightapplied_inbaselineVrange_list.append(cell_name)

    if (cell_name in has_neatevents_list) and (cell_name in has_lightapplied_inbaselineVrange_list):
        depolarizingeventsfile_name = cell_name + '_depolarizing_events.csv'
        depolarizingevents_df = pd.read_csv((results_path+'\\'+depolarizingeventsfile_name))
        neat_blocks_fileorigins = depolarizingevents_df.file_origin[depolarizingevents_df.neat_event].unique()
        ttlon_file_origins = subthreshold_responses.file_origin
        if sum(ttlon_file_origins.isin(neat_blocks_fileorigins)) > 0:
            neat_ttlon_traces = subthreshold_responses[ttlon_file_origins.isin(neat_blocks_fileorigins)]
            neat_ttlon_traces.plot.scatter('baselinev', 'response_maxdvdt')
            plt.title(cell_name + ' neat files only')
            neuron_data = SingleNeuron(cell_name)
            neuron_data.plot_rawdatatraces_ttlaligned(*neat_ttlon_traces.file_origin.unique())


# %%
# interesting neurons:
# 190527A,
# 190529A1 - twin to 190527A
# 190529B - has a fastevent of 20mV amplitude?
# 190529D - fastevent (20mV) = AIS spike?
# 200630B2 - very nice resemblance between spont. and light-evoked APs
# 200630D - gets hyperpolarized quite far, still firing APs (also spont); no DC-evoked APs
# 200701A - twin to 200630D
# 200708D - light activations get smaller amp with hyperpolarization, until fastevent disappears
# 201125C - example of neuron without any fastevents?
# 201125D - our favorite example of light-activated synapse and spont.fastevent
# 210110F - just looks nice
# 210113D - spont.APs at baselinev=-60mV without shoulder
# 210113H - two different amp fastevents activated by light (riding very small synapse)
# 210124B - fastevent+degenerate AIS spike?














