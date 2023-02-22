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
recordings_dfs_list = [recordings_Thy1, recordings_RBP, recordings_virus_toMDJ, recordings_virus_toMidbrain]
recordings_lightactive_all = pd.concat(recordings_dfs_list)
# checked and double-checked: anatomical location data is up-to-date for all recordings, as is time_recorded_ins.
# So, these tags can be used to filter out any recordings that aren't IO or aren't real recordings (t=0):
IOneurons_recordings_t_over0 = (recordings_lightactive_all.anatomical_location == 'inferior_olive') \
                       & (recordings_lightactive_all.total_t_recorded_in_s > 0)
recordings_lightactive_IO = recordings_lightactive_all[IOneurons_recordings_t_over0]
# Total number of recorded neurons in the dataset: N = 78 (len(recordings_lightactive_IO))
# Total number of labeled mice used: n = 26 (len(expdays_lightactive_all))

# Adding a column to recordings_metadata: n segments with light on (i.e., ttl applied)
recordings_lightactive_IO.insert(loc=18, column='n_ttl_applications', value=np.nan)
resultsfiles_path = path + '\\myResults'
resultsfiles_list = os.listdir(resultsfiles_path)
for neuron in recordings_lightactive_IO.name:
    neuron_recordingblocks_index_filename = neuron + '_recordingblocks_index.csv'
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


# re-ordering the prepotential_aps_df by mean event amplitude
all_prepotential_aps_df['mean_prepotential_amp'] = np.nan
for neuron in all_prepotential_aps_df.neuron_name.unique():
    mean_amp = all_prepotential_aps_df[all_prepotential_aps_df.neuron_name == neuron].ap_prepotential_amp.mean()
    all_prepotential_aps_df.loc[(all_prepotential_aps_df.neuron_name == neuron), 'mean_prepotential_amp'] = mean_amp
all_prepotential_aps_df = all_prepotential_aps_df.sort_values('mean_prepotential_amp')
# filtering down to 'neat' APs only and doing it again:
neat_prepotential_aps_df = all_prepotential_aps_df[all_prepotential_aps_df.neat_event]
neat_prepotential_aps_df['mean_prepotential_amp'] = np.nan
for neuron in neat_prepotential_aps_df.neuron_name.unique():
    mean_amp = neat_prepotential_aps_df[neat_prepotential_aps_df.neuron_name == neuron].ap_prepotential_amp.mean()
    neat_prepotential_aps_df.loc[(neat_prepotential_aps_df.neuron_name == neuron), 'mean_prepotential_amp'] = mean_amp
neat_prepotential_aps_df = neat_prepotential_aps_df.sort_values('mean_prepotential_amp')


# function for getting data only from neurons that have at least N APs with prepotential (APs category (spont/evoked//neat/all) determined by subsection of prepotential_aps_df the function is run on):
def get_atleast_n_df_byneuronname(df, atleast_n):
    for neuron in df.neuron_name.unique():
        neuron_df = df[df.neuron_name == neuron]
        if len(neuron_df) < atleast_n:
            df.drop(neuron_df.index, inplace=True)
    return df

# %% create dataframe: means/stds per neuron

# %% FIGURE PANELS
# %% Histograms of %APs from prepotentials in the population of recorded neurons
bins = np.arange(start=0, stop=105, step=5).tolist()  # 20 evenly spaced bins from 0 to 100%

# spont, all APs
n_aps_df.hist(column='spont_percentwithprepotential',
                   # by='mouse_type',
                   sharex=True, sharey=True,
                   bins=bins)
plt.xlim([0, 100])
plt.ylim(([0, 7]))
# spont, neat APs only
n_aps_df.hist(column='neat_spont_percentwithprepotential',
                   # by='mouse_type',
                   sharex=True, sharey=True,
                   bins=bins)
plt.xlim([0, 100])
plt.ylim(([0, 7]))

# light-evoked, all APs
n_aps_df.hist(column='evoked_percentwithprepotential',
              sharex=True, sharey=True,
              bins=bins)
plt.xlim([0, 100])
plt.ylim([0, 7])
# light-evoked, neat APs only
n_aps_df.hist(column='neat_evoked_percentwithprepotential',
                   # by='mouse_type',
                   sharex=True, sharey=True,
                   bins=bins)
plt.xlim([0, 100])
plt.ylim(([0, 7]))

# %% Plots of prepotential amplitudes in the population of recorded neurons
# all neurons/APs: stripplot of prepotential amplitudes, split out by spont/evoked
# sns.catplot(
#     data=neat_prepotential_aps_df,
#     x="ap_prepotential_amp",
#     y="neuron_name",
#     hue="applied_ttlpulse",
#     kind="strip"
#     # kind="violin",
#     # scale='count',
#     # cut=0,
#     # bw=0.1,
#     # inner="stick", split=True,
# )
atleast_n = 2
# separately for spont. and evoked APs:
# spont, neat only:
neat_spont_prepotential_aps_df = neat_prepotential_aps_df[~neat_prepotential_aps_df.applied_ttlpulse]
neat_spont_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_spont_prepotential_aps_df, atleast_n)
sns.catplot(
    data=neat_spont_prepotential_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    kind="strip"
)
plt.title('neat spont.APs')
plt.xlim([0, 35])
# spont, all:
spont_prepotential_aps_df = all_prepotential_aps_df[~all_prepotential_aps_df.applied_ttlpulse]
spont_prepotential_aps_df = get_atleast_n_df_byneuronname(spont_prepotential_aps_df, atleast_n)
sns.catplot(
    data=spont_prepotential_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    kind="strip"
)
plt.title('all spont.APs')
plt.xlim([0, 35])

# evoked, neat only:
neat_evoked_prepotential_aps_df = neat_prepotential_aps_df[neat_prepotential_aps_df.applied_ttlpulse]
neat_evoked_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_evoked_prepotential_aps_df, atleast_n)
sns.catplot(
    data=neat_evoked_prepotential_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    kind="strip"
)
plt.title('neat evoked APs')
plt.xlim([0, 35])
# evoked, all:
evoked_prepotential_aps_df = all_prepotential_aps_df[all_prepotential_aps_df.applied_ttlpulse]
evoked_prepotential_aps_df = get_atleast_n_df_byneuronname(evoked_prepotential_aps_df, atleast_n)
sns.catplot(
    data=evoked_prepotential_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    kind="strip"
)
plt.title('evoked APs')
plt.xlim([0, 35])

# only neurons that have at least two of both spont. and evoked neat APs with prepotentials:
n_aps = 2
neat_evokedandspont_dfslist = []
for neuron in neat_prepotential_aps_df.neuron_name.unique():
    neuron_aps_df = neat_prepotential_aps_df[neat_prepotential_aps_df.neuron_name == neuron]
    if (sum(neuron_aps_df.applied_ttlpulse) >= n_aps) and (sum(~neuron_aps_df.applied_ttlpulse) >= n_aps):
        neat_evokedandspont_dfslist.append(neuron_aps_df)
neat_evokedandspont_aps_df = pd.concat(neat_evokedandspont_dfslist)

sns.catplot(
    data=neat_evokedandspont_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    hue="applied_ttlpulse",
    kind="strip",
)
plt.title('neurons with at least two of neat spont. and evoked APs with prepotential')
plt.xlim([0, 35])

# neurons that have at least two of both spont. and evoked APs with prepotentials (non-neat):
evokedandspont_dfslist = []
for neuron in all_prepotential_aps_df.neuron_name.unique():
    neuron_aps_df = all_prepotential_aps_df[all_prepotential_aps_df.neuron_name == neuron]
    if (sum(neuron_aps_df.applied_ttlpulse) >= n_aps) and (sum(~neuron_aps_df.applied_ttlpulse) >= n_aps):
        evokedandspont_dfslist.append(neuron_aps_df)
evokedandspont_aps_df = pd.concat(evokedandspont_dfslist)

sns.catplot(
    data=evokedandspont_aps_df,
    x="ap_prepotential_amp",
    y="neuron_name",
    hue="applied_ttlpulse",
    kind="strip",
)
plt.title('neurons with at least two of spont. and evoked APs with prepotential')

plt.xlim([0, 35])

# %% Plotting prepotential-to-APpeak time, also relative to ttl-to-APpeak time for evoked APs




neat_evoked_prepotential_aps_df = neat_prepotential_aps_df[neat_prepotential_aps_df.applied_ttlpulse]
neat_evoked_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_evoked_prepotential_aps_df, atleast_n)

plot = sns.catplot(
    data=neat_prepotential_aps_df,
    x="neuron_name",
    y="prepotential_to_ap_peak_time_inms",
    hue="applied_ttlpulse",
    kind="bar"
)
sns.stripplot(
    data=neat_prepotential_aps_df,
    x="neuron_name",
    y="prepotential_to_ap_peak_time_inms",
    hue="applied_ttlpulse",
    dodge=True,
    ax=plot.ax
)

# %%
neat_evoked_prepotential_aps_df = neat_prepotential_aps_df[neat_prepotential_aps_df.applied_ttlpulse]
neat_evoked_prepotential_aps_df = get_atleast_n_df_byneuronname(neat_evoked_prepotential_aps_df, atleast_n)
plot = sns.catplot(
    data=neat_evoked_prepotential_aps_df,
    x="neuron_name",
    y="lightevokedAP_ttl_to_peak",
    kind="bar"
)
sns.stripplot(
    data=neat_evoked_prepotential_aps_df,
    x="neuron_name",
    y="lightevokedAP_ttl_to_peak",
    ax=plot.ax
)

# mean and variance in the population







# %% checking over the dataset - neatevents marked
has_neatevents_list = []
has_no_neatevents_list = []

for neuron_name in recordings_lightactive_IO.name:
    filename = [filename for filename in resultsfiles_depolarizingevents if neuron_name in filename][0]  # this works because all neurons in the lightactive-dataset have a neuron_depolarizingevents-file saved in the myResults folder
    filepath = results_path + '\\' + filename
    neuron_depolarizingevents = pd.read_csv(filepath)
    if ('neat_event' in neuron_depolarizingevents.columns):
        has_neatevents_list.append(neuron_name)
    else:
        has_no_neatevents_list.append(neuron_name)

has_no_neatevents_list = ['20190527C',  # justified why not
                          '20190529A2', # justified why not
                          '20190529C',  # justified why not
                          '20190529D',  # justified why not
                          '20190529E',  # justified why not
                          '20200630A',  # added (evokedAPs)
                          '20200630B1', # justified why not
                          '20200630B2', # added (evokedAPs)
                          '20200701B',  # justified why not
                          '20200701D',  # justified why not
                          '20200706A',  # justified why not
                          '20200706D',  # justified why not
                          '20200706E',  # justified why not
                          '20200707E',  # justified why not
                          '20200708A',  # justified why not
                          '20200708C',  # justified why not
                          '20200708G',  # justified why not
                          '20210105A',  # justified why not
                          '20210105B',  # justified why not
                          '20210105C',  # justified why not
                          '20210105D',  # justified why not
                          '20210105E',  # justified why not
                          '20210429B',  # justified why not
                          '20200818C',  # justified why not
                          '20200819A',  # justified why not
                          '20201124C',  # justified why not
                          '20201125E',  # justified why not
                          '20201125F',  # justified why not
                          '20210411A',  # justified why not
                          '20210411B',  # justified why not
                          '20210411C',  # justified why not
                          '20210411F',  # justified why not
                          '20210413A',  # justified why not
                          '20210413B',  # justified why not
                          '20210426B',  # justified why not
                          '20210426C',  # justified why not
                          '20210426E',  # justified why not
                          '20210110B',  # justified why not
                          '20210110C',  # justified why not
                          '20210110F',  # justified why not
                          '20210113A',  # justified why not
                          '20210113B',  # justified why not
                          '20210113E',  # added (two spont.APs)
                          '20210113F',  # justified why not
                          '20210123B',  # justified why not
                          '20210124C',  # justified why not
                          '20210124D',  # justified why not
                          '20210203A']  # justified why not



