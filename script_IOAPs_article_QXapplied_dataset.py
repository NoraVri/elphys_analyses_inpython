# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import singleneuron_plotting_functions as plots

path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')  # metadata on each recording
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')  # metadata on the experiment day - mouse type etc. that is the same for all neurons recorded on that day

# in this script: analysis and plotting of QX-314-applied experiments
# Dataset: neurons recorded with QX-314 in the pipette.
# Different concentrations and configurations (in some experiments, pipette tip was filled with QX-free intra to get
# a time-delayed effect); this information will have to be recovered manually per neuron from experiment-day notes.

# Getting experiment-day metadata for days on which QX-314 was used:
qx_experimentdays_metadata = experimentdays_metadata[experimentdays_metadata.specialchemicals_type.str.contains('QX-314', na=False)]
# Getting recordings metadata for neurons recorded on those days:
qxdays_recordings_metadata = recordings_metadata[recordings_metadata.date.isin(qx_experimentdays_metadata.date)]
# On all experiment days where QX was applied, at least one neuron was patched without QX to see that proper APs are present.
# Getting recordings metadata for only neurons that were patched with QX in the pipette:
qxpatched_recordings_metadata = qxdays_recordings_metadata[((qxdays_recordings_metadata.elphysrecording_notes.str.contains('QX', na=False))
                                                            & (qxdays_recordings_metadata.total_t_recorded_in_s > 0))]
# Recordings performed in 2022-05 all had low QX concentration (~0.3mM);
# Recordings performed in 2022-12 were done with tip filled with QX-free intra (with varying success; in some cases
# QX-containing intra could be seen to come out of the pipette before the neuron was patched; in other cases neurons
# died before QX-containing intra reached them).
# Experiment-day notes on neurons where I attempted patching with QX-free intra in the tip of the pipette:
# 20221227C - died before QX-intra could be seen to reach the recorded neuron
# 20221227D - died while stimulating electrode was moving around; not sure whether QX reached the neuron
# 20221227E - QX-intra could be seen coming out of the pipette faintly just before patching the neuron; neuron was filled with QX-intra within 15 minutes from establishing patch
# 20221227F - QX-intra could be seen coming out of the pipette clearly before patching the neuron
# 20221227G - soma faintly labeled in QX-color by the time neuron died quickly and suddenly (~15 minutes after establishing patch); however, the last 8 sweeps of recorded data had to be excluded, and it seems that in the 5 minutes before that the neuron was able to make Na-spikes throughout..
# 20221229C - soma labeled in QX-color by file electricalStim#5
# 20221229D - both colors could be seen to come out of the pipette before patching; neuron labeled in both colors by file GapFree#1
# 20221229E - it took at least ~10 minutes for QX-intra to reach the recorded neuron
# 20221229F - died after ~5min. of recording, no visible fluorescent labeling in either color

# Based on these notes, neurons 20221227C, 20221227D, 20221227G and 20221229F should be excluded from the QX-patched dataset
# because QX (probably) did not actually reach the recorded neurons.
to_drop = ['20221227C', '20221227D', '20221227G', '20221229F']
qxpatched_recordings_metadata = qxpatched_recordings_metadata[~qxpatched_recordings_metadata.name.isin(to_drop)]

# %% getting mean events frequencies in the first and last 5 minutes of recording for neurons in the QX-dataset
# and showing them in a plot

def get_meaneventfreq_infirstandlast5min(recordingblocksindex_df):
    t_count_fromstart = 0
    first5min_blocks = []
    sorted_ascending = recordingblocksindex_df.sort_values('file_timestamp')
    for idx, row in sorted_ascending.iterrows():
        while t_count_fromstart < 600:
            t_count_fromstart += row.t_recorded_ins
            first5min_blocks.append(row.file_origin)
    first5min_df = recordingblocksindex_df[recordingblocksindex_df.file_origin.isin(first5min_blocks)]
    first5min_meanAPfreq = first5min_df.spontaps_avgfreqs.mean()
    first5min_meanfasteventfreq = first5min_df.spontfastevents_avgfreqs.mean()

    t_count_fromend = 0
    last5min_blocks = []
    sorted_descending = recordingblocksindex_df.sort_values('file_timestamp', ascending=False)
    for idx, row in sorted_descending.iterrows():
        while t_count_fromend < 300:
            t_count_fromend += row.t_recorded_ins
            last5min_blocks.append(row.file_origin)
    last5min_df = recordingblocksindex_df[recordingblocksindex_df.file_origin.isin(last5min_blocks)]
    last5min_meanAPfreq = last5min_df.spontaps_avgfreqs.mean()
    last5min_meanfasteventfreq = last5min_df.spontfastevents_avgfreqs.mean()
    return first5min_meanAPfreq, first5min_meanfasteventfreq, last5min_meanAPfreq, last5min_meanfasteventfreq

resultsfiles_path = path + '\\myResults'
meaneventsfreqs_infos = {
        'neuron_name': [],
        'first5min_meanAPfreq': [],
        'first5min_meanfasteventfreq': [],
        'last5min_meanAPfreq': [],
        'last5min_meanfasteventfreq': [],
    }

for neuron in qxpatched_recordings_metadata.name:
    neuron_recordingblocks_index_filename = neuron + '_recordingblocks_index.csv'
    neuron_recordingblocks_index = pd.read_csv(resultsfiles_path + '\\' + neuron_recordingblocks_index_filename)
    (first5min_meanAPfreq, first5min_meanfasteventfreq,
     last5min_meanAPfreq, last5min_meanfasteventfreq) = get_meaneventfreq_infirstandlast5min(neuron_recordingblocks_index)
    meaneventsfreqs_infos['neuron_name'].append(neuron)
    meaneventsfreqs_infos['first5min_meanAPfreq'].append(first5min_meanAPfreq)
    meaneventsfreqs_infos['first5min_meanfasteventfreq'].append(first5min_meanfasteventfreq)
    meaneventsfreqs_infos['last5min_meanAPfreq'].append(last5min_meanAPfreq)
    meaneventsfreqs_infos['last5min_meanfasteventfreq'].append(last5min_meanfasteventfreq)

# plotting mean events frequencies as barplots with individual datapoints overlaid
meaneventsfreqs_df = pd.DataFrame(meaneventsfreqs_infos).round(decimals=2)
sns.stripplot(data=meaneventsfreqs_df)
sns.barplot(data=meaneventsfreqs_df)

# %% plots: raw recording traces from example neuron
neuron_data = SingleNeuron('20221229E')
des_df = neuron_data.depolarizing_events
sorted_recordingblocksindex = neuron_data.recordingblocks_index.sort_values('file_timestamp')
spont_aps = ((des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse) & (des_df.baselinev < -30))  # adding baselineV criterion because there are some APs riding depolarizing current pulses in this trace (they all come >40ms after currentpulsechange, but the slow ramping up of baselineV there would make it hard to say what exactly they are evoked by)
spont_fastevents = (des_df.event_label == 'fastevent') & (~des_df.applied_ttlpulse)
# neuron_data.plot_rawdatablocks('gapFree', events_to_mark=(spont_aps | spont_fastevents))
# %%
# plots:
# first 30s of the first and last gapFree recording files;
# insets: zoom-in to show events.
# gapFree#0 60-64s, and a plot of collected spont.APs and fastevents in the first 5 min;
# gapFree#2 110-140s, zoom-in further on two spikelets

# early 5 minutes: examples of events
# long (30s) trace
figure1, axes1 = neuron_data.plot_rawdatablocks('gapFree_0000', events_to_mark=(spont_aps | spont_fastevents))
axes1[0].set_xlim(57000, 87000)
axes1[0].set_ylim(-62, 50)
# zoom-in:
axes1[0].set_xlim(60000, 64000)
# plot of events in the first 5 minutes
first5min_events = ((spont_aps | spont_fastevents) & (des_df.file_origin.isin(['gapFree_0000.abf', 'electricalStim_0000.abf'])))
neuron_data.plot_depolevents(first5min_events,
                             prealignpoint_window_inms=3,
                             plotwindow_inms=8)

# late 5 minutes: examples
# long (30s) trace
figure2, axes2 = neuron_data.plot_rawdatablocks('gapFree_0002', events_to_mark=(spont_aps | spont_fastevents))
axes2[0].set_xlim(110000, 140000)
axes2[0].set_ylim(-43.5, -40.5)
# zoom-in: 500ms with a bunch of spikelets in it
axes2[0].set_xlim(116400, 117100)
