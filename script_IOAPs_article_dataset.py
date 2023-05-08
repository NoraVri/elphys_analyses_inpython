# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# In this script: analysis of APs as triggered from fast-events.
# Dataset: IO neurons recorded from brainstem slices of mice with optogenetically activatable axons from elsewhere in the brain.

# AP-prepotential calculation has been run with default function parameters for all events labeled "actionpotential" in neuron_deolarizingevents-dataframes.

# %% DATA TABLES
# %% metadata imports
path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')  # metadata on each recording
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')  # metadata on the experiment day - mouse type etc. that is the same for all neurons recorded on that day

# %% Defining the dataset - IO neuron recordings from mice with optogenetically activateable inputs
# Getting all experiment days that optogenetically activatable inputs were in the slice,
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

# Getting IO neuron recordings from days that optogenetically activatable inputs were in the slice
# per input type, and adding mouse type from experiment_days to recordings_metadata
recordings_virus_toMidbrain = recordings_metadata[(recordings_metadata.date.isin(expdays_virus_toMidbrain))]
recordings_virus_toMidbrain['mouse_type'] = 'virus_toMidbrain'
recordings_virus_toMDJ = recordings_metadata[(recordings_metadata.date.isin(expdays_virus_toMDJ))]
recordings_virus_toMDJ['mouse_type'] = 'virus_toMDJ'
recordings_RBP = recordings_metadata[(recordings_metadata.date.isin(expdays_RBP))]
recordings_RBP['mouse_type'] = 'RBP'
recordings_Thy1 = recordings_metadata[(recordings_metadata.date.isin(expdays_Thy1))]
recordings_Thy1['mouse_type'] = 'Thy1'
# adding them all together again into collected dataframes
expdays_lightactive_all = pd.concat([expdays_virus_toMidbrain, expdays_virus_toMDJ, expdays_RBP, expdays_Thy1])
recordings_lightactive_all = pd.concat([recordings_Thy1, recordings_RBP, recordings_virus_toMDJ, recordings_virus_toMidbrain])
# checked and double-checked: anatomical location data is up-to-date for all recordings, as is time_recorded_ins.
# So, these tags can be used to filter out any recordings that aren't IO or aren't real recordings (t=0):
IOneurons_recordings_t_over0 = ((recordings_lightactive_all.anatomical_location == 'inferior_olive')
                                & (recordings_lightactive_all.total_t_recorded_in_s > 0))
recordings_lightactive_IO = recordings_lightactive_all[IOneurons_recordings_t_over0]
# Total number of recorded neurons in the dataset: N = 78 (len(recordings_lightactive_IO))
# Total number of labeled mice used: n = 26 (len(expdays_lightactive_all))

# Adding a column to recordings_metadata: n segments with light on (i.e., ttl applied)
recordings_lightactive_IO.insert(loc=18, column='n_ttl_applications', value=np.nan)
resultsfiles_path = path + '\\myResults'
resultsfiles_list = os.listdir(resultsfiles_path)
for neuron in recordings_lightactive_IO.name:
    neuron_recordingblocks_index_filename = neuron + '_recordingblocks_index.csv'  # the recordingblocks_index of each neurons contains information per recordingblock on whether TTL was applied; and if yes, how many segments (= repetitions; in my recordings there is only 1 light application per segment).
    neuron_recordingblocks_index = pd.read_csv(resultsfiles_path + '\\' + neuron_recordingblocks_index_filename)
    if sum(neuron_recordingblocks_index.ttl_record) > 0:
        n_lightapplications = sum(neuron_recordingblocks_index[neuron_recordingblocks_index.ttl_record].n_segments)
        recordings_lightactive_IO.loc[(recordings_lightactive_IO.name == neuron), 'n_ttl_applications'] = n_lightapplications

# Getting recordings_metadata for neurons with light applications only:
recordings_lightactive_IO_ttlapplied = recordings_lightactive_IO[~(recordings_lightactive_IO.n_ttl_applications.isna())]
# Total number of neurons with light applications in the dataset: N = 69 (len(recordings_lightactive_IO_ttlapplied))
# Smallest number of light applications in one neuron: 5 (recordings_lightactive_IO.n_ttl_applications.min())
# shortest recording is just under 3 minutes (recordings_lightactive_IO_ttlapplied.total_t_recorded_in_s.min() / 60)
#  5 neurons have recording shorter than 5 minutes (recordings_lightactive_IO_ttlapplied[~(recordings_lightactive_IO_ttlapplied.total_t_recorded_in_s > 300)].name)


# %% create dataframe: APs from prepotentials - per neuron, aggregate numbers and percentages
# In this section: collecting numbers of APs evoked from prepotential by looping over depolarizing_events-resultsfiles
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
for neuron_name in recordings_lightactive_IO.name:
    filename = [filename for filename in resultsfiles_depolarizingevents if neuron_name in filename][0]  # this works because all neurons in the lightactive-dataset have a neuron_depolarizingevents-file saved in the myResults folder
    filepath = results_path + '\\' + filename
    neuron_depolarizingevents = pd.read_csv(filepath)
    aps = neuron_depolarizingevents.event_label == 'actionpotential'
    if ('ap_prepotential_amp' in neuron_depolarizingevents.columns):
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

# Getting percentages of APs from prepotential:
n_aps_df['spont_percentwithprepotential'] = np.nan
n_aps_df['neat_spont_percentwithprepotential'] = np.nan
n_aps_df['evoked_percentwithprepotential'] = np.nan
n_aps_df['neat_evoked_percentwithprepotential'] = np.nan
for index, row in n_aps_df.iterrows():
    if row.n_spontAPs > 0:
        n_aps_df.loc[index, 'spont_percentwithprepotential'] = ((row.n_spontAPs_withprepotential / row.n_spontAPs) * 100)
    if row.n_neatspontAPs > 0:
        n_aps_df.loc[index, 'neat_spont_percentwithprepotential'] = ((row.n_neatspontAPs_withprepotential / row.n_neatspontAPs) * 100)
    if row.n_evokedAPs > 0:
        n_aps_df.loc[index, 'evoked_percentwithprepotential'] = ((row.n_evokedAPs_withprepotential / row.n_evokedAPs) * 100)
    if row.n_neatevokedAPs > 0:
        n_aps_df.loc[index, 'neat_evoked_percentwithprepotential'] = ((row.n_neatevokedAPs_withprepotential / row.n_neatevokedAPs) * 100)

# %% create dataframe: recordingblocks_indexes - info (most importantly sampling freq) per recordingblock per neuron, to be used below.
resultsfiles_recordingblocksindexes = [filename for filename in resultsfiles_all if 'recordingblocks_index' in filename]
all_recordingblocksindexes_forconcatenation = []
for neuron_name in recordings_lightactive_IO.name:
    filename = [filename for filename in resultsfiles_recordingblocksindexes if neuron_name in filename][0]
    filepath = results_path + '\\' + filename
    neuron_recordingblocks_index = pd.read_csv(filepath)
    neuron_recordingblocks_index['neuron_name'] = neuron_name
    all_recordingblocksindexes_forconcatenation.append(neuron_recordingblocks_index)
all_recordingblocks_indexes_df = pd.concat(all_recordingblocksindexes_forconcatenation)

# %% create dataframe: all data on all APs with prepotentials recorded from all neurons in the dataset
all_aps_dfs_for_concatenation = []
for neuron_name in recordings_lightactive_IO.name:
    filename = [filename for filename in resultsfiles_depolarizingevents if neuron_name in filename][0]  # this works because all neurons in the lightactive-dataset have a neuron_depolarizingevents-file saved in the myResults folder
    filepath = results_path + '\\' + filename
    neuron_depolarizingevents = pd.read_csv(filepath)
    if ('ap_prepotential_amp' in neuron_depolarizingevents.columns):
        neuron_apswithprepotential = neuron_depolarizingevents[~neuron_depolarizingevents.ap_prepotential_amp.isna()]
        neuron_apswithprepotential['neuron_name'] = neuron_name
        all_aps_dfs_for_concatenation.append(neuron_apswithprepotential)
all_prepotential_aps_df = pd.concat(all_aps_dfs_for_concatenation)
# applying some cleanups:
all_prepotential_aps_df = all_prepotential_aps_df.iloc[:, 1:59]  # the first column of the resulting df is a copy of the index column and the final (60th) column is named "applied_ttlpulse" and filled with nans for some reason, even while the applied_ttlpulse-column with actual values gets copied over just fine.
neatevent_nans = all_prepotential_aps_df.neat_event.isna()  # neatevent-column comes up containing True/False/nan, where nan should be considered False
all_prepotential_aps_df.loc[neatevent_nans, 'neat_event'] = False  # neurons that do not have any 'neat events' marked get into the df with na values in this column instead
all_prepotential_aps_df.reset_index(inplace=True)
all_prepotential_aps_df.drop(labels='index', axis=1, inplace=True)

# adding data column: time between prepotential-point and AP peak for each AP with measured prepotential
all_prepotential_aps_df['prepotential_to_ap_peak_time_inms'] = np.nan
for idx, ap_row in all_prepotential_aps_df.iterrows():
    file_samplingfreq = all_recordingblocks_indexes_df[((all_recordingblocks_indexes_df.neuron_name == ap_row.neuron_name)
                                                        & (all_recordingblocks_indexes_df.file_origin == ap_row.file_origin))].sampling_freq_inHz
    prepotential_to_ap_peak_inidcs = ap_row.peakv_idx - ap_row.ap_prepotential_idx
    prepotential_to_ap_peak_inms = float((prepotential_to_ap_peak_inidcs / file_samplingfreq) * 1000)
    all_prepotential_aps_df.loc[idx, 'prepotential_to_ap_peak_time_inms'] = prepotential_to_ap_peak_inms

# adding data column: time between TTL-onset and AP peak for each light-evoked AP with measured prepotential
ttlon_measures_files = [file for file in resultsfiles_all if 'ttlon' in file]
all_prepotential_aps_df['lightevokedAP_ttl_to_peak'] = np.nan
# all_prepotential_aps_df['lightevokedAP_ttl_to_peak_2'] = np.nan
for idx, ap_row in all_prepotential_aps_df.iterrows():
    if ap_row.applied_ttlpulse:
        # getting ttl-to-peak time as saved in the ttlon_measures tables
        neuron_name = ap_row.neuron_name
        filename = [filename for filename in ttlon_measures_files if neuron_name in filename][0]
        filepath = results_path + '\\' + filename
        neuron_tttlonmeasures = pd.read_csv(filepath)
        ap_ttlonmeasures = neuron_tttlonmeasures[((neuron_tttlonmeasures.file_origin == ap_row.file_origin)
                                                  & (neuron_tttlonmeasures.segment_idx == ap_row.segment_idx))]
        ttl_to_responsemaxamp = float(ap_ttlonmeasures.response_maxamp_postttl_t_inms)
        all_prepotential_aps_df.loc[idx, 'lightevokedAP_ttl_to_peak'] = ttl_to_responsemaxamp
        # getting it by subtracting ttlon_idx from AP peakv_idx - I checked, comes out to the exact same number as the calculation done in get_ttlon_measures()
        # file_samplingfreq = all_recordingblocks_indexes_df[
        #     ((all_recordingblocks_indexes_df.neuron_name == ap_row.neuron_name)
        #      & (all_recordingblocks_indexes_df.file_origin == ap_row.file_origin))].sampling_freq_inHz
        # ttlon_idx = ap_ttlonmeasures.ttlon_idx
        # ap_peakidx = ap_row.peakv_idx
        # ttlon_to_appeak_inidcs = ap_peakidx - int(ttlon_idx)
        # ttlon_to_appeak_inms = float((ttlon_to_appeak_inidcs / file_samplingfreq) * 1000)
        # all_prepotential_aps_df.loc[idx, 'lightevokedAP_ttl_to_peak_2'] = ttlon_to_appeak_inms

# Generally, we will be using data from 'neat' stretches of neuron recordings for figure panels; filtering down:
neat_prepotential_aps_df = all_prepotential_aps_df[all_prepotential_aps_df.neat_event]

# FUNCTIONS for getting subsets of the n_aps_df:
# function for getting data only from neurons that have at least N APs with prepotential (APs category (spont/evoked//neat/all) determined by subsection of prepotential_aps_df the function is run on):
def get_atleast_n_df_byneuronname(df, atleast_n):
    for neuron in df.neuron_name.unique():
        neuron_df = df[df.neuron_name == neuron]
        if len(neuron_df) < atleast_n:
            df.drop(neuron_df.index, inplace=True)
    return df

# function for getting data only from neurons that have at least N APs with prepotential both spont. and evoked (neat/non-neat APs category determined by subsection of prepotential_aps_df the function is run on):
def get_atleast_n_ofeach_df_byneuronname(df, atleast_n):
    dfs_list = []
    for neuron in df.neuron_name.unique():
        neuron_df = df[df.neuron_name == neuron]
        neuron_n_appliedttl_aps = sum(neuron_df.applied_ttlpulse)
        neuron_n_spont_aps = sum(~neuron_df.applied_ttlpulse)
        if ((neuron_n_spont_aps >= atleast_n) & (neuron_n_appliedttl_aps >= atleast_n)):
            dfs_list.append(neuron_df)
    new_df = pd.concat(dfs_list)
    return new_df


# %% Adding columns to the n_aps_df: means/stds per neuron for three different to-APpeak-time measures
# (1) prepotential-to-peak time for spont.APs; (2) prepotential-to-peak time for evokedAPs; (3) TTL-to-peak time for evokedAPs.

n_aps_df['spont_prepotential_to_appeak_time_mean'] = np.nan
n_aps_df['spont_prepotential_to_appeak_time_std'] = np.nan
n_aps_df['evoked_prepotential_to_appeak_time_mean'] = np.nan
n_aps_df['evoked_prepotential_to_appeak_time_std'] = np.nan
n_aps_df['evoked_ttl_to_appeak_time_mean'] = np.nan
n_aps_df['evoked_ttl_to_appeak_time_std'] = np.nan
n_aps_df['neat_spont_prepotential_to_appeak_time_mean'] = np.nan
n_aps_df['neat_spont_prepotential_to_appeak_time_std'] = np.nan
n_aps_df['neat_evoked_prepotential_to_appeak_time_mean'] = np.nan
n_aps_df['neat_evoked_prepotential_to_appeak_time_std'] = np.nan
n_aps_df['neat_evoked_ttl_to_appeak_time_mean'] = np.nan
n_aps_df['neat_evoked_ttl_to_appeak_time_std'] = np.nan

for index, row in n_aps_df.iterrows():
    neuron_name = row.neuron_name
    neuron_prepotentialaps = all_prepotential_aps_df[all_prepotential_aps_df.neuron_name == neuron_name]
    if row.n_spontAPs_withprepotential > 0:
        neuron_spontaps = neuron_prepotentialaps[~neuron_prepotentialaps.applied_ttlpulse]
        n_aps_df.loc[index, 'spont_prepotential_to_appeak_time_mean'] = neuron_spontaps.prepotential_to_ap_peak_time_inms.mean()
        n_aps_df.loc[index, 'spont_prepotential_to_appeak_time_std'] = neuron_spontaps.prepotential_to_ap_peak_time_inms.std()
    if row.n_evokedAPs_withprepotential > 0:
        neuron_evokedaps = neuron_prepotentialaps[neuron_prepotentialaps.applied_ttlpulse]
        n_aps_df.loc[index, 'evoked_prepotential_to_appeak_time_mean'] = neuron_evokedaps.prepotential_to_ap_peak_time_inms.mean()
        n_aps_df.loc[index, 'evoked_prepotential_to_appeak_time_std'] = neuron_evokedaps.prepotential_to_ap_peak_time_inms.std()
        n_aps_df.loc[index, 'evoked_ttl_to_appeak_time_mean'] = neuron_evokedaps.lightevokedAP_ttl_to_peak.mean()
        n_aps_df.loc[index, 'evoked_ttl_to_appeak_time_std'] = neuron_evokedaps.lightevokedAP_ttl_to_peak.std()

    neuron_neat_prepotentialaps = neuron_prepotentialaps[neuron_prepotentialaps.neat_event]
    if row.n_neatspontAPs_withprepotential > 0:
        neuron_neat_spontaps = neuron_neat_prepotentialaps[~neuron_neat_prepotentialaps.applied_ttlpulse]
        n_aps_df.loc[index, 'neat_spont_prepotential_to_appeak_time_mean'] = neuron_neat_spontaps.prepotential_to_ap_peak_time_inms.mean()
        n_aps_df.loc[index, 'neat_spont_prepotential_to_appeak_time_std'] = neuron_neat_spontaps.prepotential_to_ap_peak_time_inms.std()
    if row.n_neatevokedAPs_withprepotential > 0:
        neuron_neat_evokedaps = neuron_neat_prepotentialaps[neuron_neat_prepotentialaps.applied_ttlpulse]
        n_aps_df.loc[index, 'neat_evoked_prepotential_to_appeak_time_mean'] = neuron_neat_evokedaps.prepotential_to_ap_peak_time_inms.mean()
        n_aps_df.loc[index, 'neat_evoked_prepotential_to_appeak_time_std'] = neuron_neat_evokedaps.prepotential_to_ap_peak_time_inms.std()
        n_aps_df.loc[index, 'neat_evoked_ttl_to_appeak_time_mean'] = neuron_neat_evokedaps.lightevokedAP_ttl_to_peak.mean()
        n_aps_df.loc[index, 'neat_evoked_ttl_to_appeak_time_std'] = neuron_neat_evokedaps.lightevokedAP_ttl_to_peak.std()


# %% FIGURE PANELS
# %% Plots of prepotential amplitudes in the population of recorded neurons

# adding min. and mean prepotential amp values (per neuron) as df column, for sorting by:
# all APs:
all_prepotential_aps_df['mean_prepotential_amp'] = np.nan
all_prepotential_aps_df['min_prepotential_amp'] = np.nan
for neuron in all_prepotential_aps_df.neuron_name.unique():
    mean_amp = all_prepotential_aps_df[all_prepotential_aps_df.neuron_name == neuron].ap_prepotential_amp.mean()
    all_prepotential_aps_df.loc[(all_prepotential_aps_df.neuron_name == neuron), 'mean_prepotential_amp'] = mean_amp
    min_amp = all_prepotential_aps_df[all_prepotential_aps_df.neuron_name == neuron].ap_prepotential_amp.min()
    all_prepotential_aps_df.loc[(all_prepotential_aps_df.neuron_name == neuron), 'min_prepotential_amp'] = min_amp
# 'neat' APs only:
neat_prepotential_aps_df['mean_prepotential_amp'] = np.nan
for neuron in neat_prepotential_aps_df.neuron_name.unique():
    mean_amp = neat_prepotential_aps_df[neat_prepotential_aps_df.neuron_name == neuron].ap_prepotential_amp.mean()
    neat_prepotential_aps_df.loc[(neat_prepotential_aps_df.neuron_name == neuron), 'mean_prepotential_amp'] = mean_amp
    min_amp = neat_prepotential_aps_df[neat_prepotential_aps_df.neuron_name == neuron].ap_prepotential_amp.min()
    neat_prepotential_aps_df.loc[(neat_prepotential_aps_df.neuron_name == neuron), 'min_prepotential_amp'] = min_amp

# For neat and evoked APs separately, filter down to neurons that have at least two
atleast_n = 2
# all APs, spont:
spont_prepotential_aps_df = all_prepotential_aps_df[~all_prepotential_aps_df.applied_ttlpulse]
spont_prepotential_aps_df = get_atleast_n_df_byneuronname(spont_prepotential_aps_df, atleast_n)
# all APs, evoked:
evoked_prepotential_aps_df = all_prepotential_aps_df[all_prepotential_aps_df.applied_ttlpulse]
evoked_prepotential_aps_df = get_atleast_n_df_byneuronname(evoked_prepotential_aps_df, atleast_n)
# 'neat' APs only, spont:
neat_spont_prepotential_aps_df = neat_prepotential_aps_df[~neat_prepotential_aps_df.applied_ttlpulse]
neat_spont_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_spont_prepotential_aps_df, atleast_n)
# 'neat' APs only, evoked:
neat_evoked_prepotential_aps_df = neat_prepotential_aps_df[neat_prepotential_aps_df.applied_ttlpulse]
neat_evoked_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_evoked_prepotential_aps_df, atleast_n)

# Sort order of neurons to plot:
all_prepotential_aps_df = all_prepotential_aps_df.sort_values('mean_prepotential_amp')
neat_prepotential_aps_df = neat_prepotential_aps_df.sort_values('mean_prepotential_amp')
# all_prepotential_aps_df = all_prepotential_aps_df.sort_values('min_prepotential_amp')
# neat_prepotential_aps_df = neat_prepotential_aps_df.sort_values('min_prepotential_amp')


# PLOTS: horizontal stripplots of AP prepotential amplitudes, for different (combinations of) groups of AP types (evoked/spont, neat/all)
# Spont. and evoked AP prepotential amplitudes in separate plots
# spont, all:
# sns.catplot(
#     data=spont_prepotential_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     kind="strip"
# )
# plt.title('all spont.APs')
# plt.xlim([0, 35])
# # evoked, all:
# sns.catplot(
#     data=evoked_prepotential_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     kind="strip"
# )
# plt.title('evoked APs')
# plt.xlim([0, 35])

# 'neat' APs only:
# spont, neat only:
# sns.catplot(
#     data=neat_spont_prepotential_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     kind="strip"
# )
# plt.title('neat spont.APs')
# plt.xlim([0, 30])
# # evoked, neat only:
# sns.catplot(
#     data=neat_evoked_prepotential_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     kind="strip"
# )
# plt.title('neat evoked APs')
# plt.xlim([0, 30])

# filtering down: only neurons that have at least two
# 'neat' APs only:
# spont, neat only:
neat_spont_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_spont_prepotential_aps_df, 2)
sns.catplot(
    data=neat_spont_prepotential_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    kind="strip"
)
plt.title('neat spont.APs, for neurons that have at least two')
plt.xlim([0, 30])
# evoked, neat only:
neat_evoked_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_evoked_prepotential_aps_df, 2)
sns.catplot(
    data=neat_evoked_prepotential_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    kind="strip"
)
plt.title('neat evoked APs, for neurons that have at least two')
plt.xlim([0, 30])


# Spont. and evoked AP prepotential amplitudes plotted together
# all APs:
# sns.catplot(
#     data=all_prepotential_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     hue="applied_ttlpulse",
#     kind="strip",
#     dodge=True,
# )
# plt.title('amplitudes of all spont. and evoked APs with prepotential')
# plt.xlim([0, 35])
# # neat only:
# sns.catplot(
#     data=neat_prepotential_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     hue="applied_ttlpulse",
#     kind="strip",
#     dodge=True,
# )
# plt.title('amplitudes of all neat spont. and evoked APs with prepotential')
# plt.xlim([0, 35])

# filtering down (neat APs only): only neurons that have at least one of each (evoked/spont)
# neat_evokedandspont_aps_df = get_atleast_n_ofeach_df_byneuronname(neat_prepotential_aps_df, 1)
# sns.catplot(
#     data=neat_evokedandspont_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     hue="applied_ttlpulse",
#     dodge=True,
#     kind="strip",
# )
# plt.title('neurons with at least one of neat spont. and evoked APs with prepotential')
# plt.xlim([0, 25])

# filtering down (neat APs only): only neurons that have at least two of each (evoked/spont)
neat_evokedandspont_aps_df = get_atleast_n_ofeach_df_byneuronname(neat_prepotential_aps_df, 2)
sns.catplot(
    data=neat_evokedandspont_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    hue="applied_ttlpulse",
    dodge=True,
    kind="strip",
)
plt.title('neurons with at least two of neat spont. and evoked APs with prepotential')
plt.xlim([0, 25])


# %% Plots of prepotential-to-APpeak times and ttl-to-APpeak times
# stripplot of prepotential-to-appeak times for neat spont.APs (in neurons that have at least two)
sns.catplot(
    data=neat_spont_prepotential_aps_df,
    x="prepotential_to_ap_peak_time_inms",
    y="neuron_name",
    kind="strip"
)
plt.title('neat spont.AP prepotential-to-peak times, for neurons that have at least two')
plt.xlim([0.5, 2])


to_appeak_times_df = n_aps_df.iloc[:,14:26]
plt.figure()
plot = sns.barplot(data=to_appeak_times_df,
                   orient='h',
                   )
sns.stripplot(data=to_appeak_times_df,
                   orient='h',
            ax=plot)

to_neat_appeak_times_df = n_aps_df.iloc[:,20:26]
plt.figure()
plot = sns.barplot(data=to_neat_appeak_times_df,
                   orient='h',
                   )
sns.stripplot(data=to_neat_appeak_times_df,
                   orient='h',
            ax=plot)

# separately for prepotential-to-APpeak times and TTL-to-APpeak times
prepotential_to_appeak_times_df = n_aps_df.iloc[:,20:24]
ttl_to_appeak_times_df = n_aps_df.iloc[:,24:26]
plt.figure()
plot = sns.barplot(data=prepotential_to_appeak_times_df,
                   orient='h',
                   errorbar='sd',
                   )
sns.stripplot(data=prepotential_to_appeak_times_df,
              orient='h', ax=plot)
plt.figure()
plot = sns.barplot(data=ttl_to_appeak_times_df,
                   orient='h',
                   errorbar='sd')
sns.stripplot(data=ttl_to_appeak_times_df,
              orient='h', ax=plot)

