# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

# importing the data
neuron_name = '20250407A1'
neuron_data = SingleNeuron(neuron_name)
# %%
# quick-and-dirty overview of data and automatically extracted spiking:
neuron_data.get_spikes_fromcellattachedrecording()
neuron_data.plot_rawdatatraces_with_cellattachedspikes()

# %% applying data cleanups
# # removing the recording channel not belonging to this neuron
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# # removing parts of the recording that do not register the neuron's behavior properly and/or muck up spike detection for some reason:
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_0000.abf',
#                                                trace_end_t=56.5)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_GluBlockers_WashIn_0000.abf',
#                                                trace_end_t=226.6)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_with_GluBlockers_gabazineWashOn_0000.abf',
#                                                trace_end_t=305)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_0000.abf',
#                                                trace_end_t=151.9)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection
# neuron_data.rawdata_remove_nonrecordingsection('gapFree_with_GluBlockers_with_gabazine_with_quinpirole_0000.abf',
#                                                trace_end_t=135.5)  # CC-to-VC switch, removing last few s of recording file (after switch) to hopefully get better baseline for spike detection

neuron_data.get_spikes_fromcellattachedrecording()
# neuron_data.plot_rawdatatraces_with_cellattachedspikes()
cellattachedspikes_df = neuron_data.cellattachedspikes
# %% for each drug/temperature condition, find 30s where spikes were picked up cleanly
# and use that to get numbers: avg.spike frequency and inter-spike-interval coefficient of variance

# %% baseline @ RT
# neuron_data.plot_rawdatatraces_with_cellattachedspikes('gapFree_0')
# manual count: 31 spikes/2s, very steady across all these recording files (total time 8.7min).
# spikes all picked up neatly for VC-recorded files (1-3) but not CC recorded files (0 and 4).
df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_0002.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx < (20000 * 30)]
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))


# %% baseline @ RT with glu-blockers
# neuron_data.plot_rawdatatraces_with_cellattachedspikes('gapFree_GluBlockers')
# manual count: 31 spikes/2s, still very steady across files
# ignore first 3 min. of first recording file (wash in); after that blockers are on (total time 12 - 3 min.)
# spikes picked up mostly neatly for file #1 (VC recording) but not the CC recorded files (0 and 2)
df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_GluBlockers_WashIn_0001.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx < (20000 * 30)]
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# looks like algorithm missed a handful of spikes (their isi's are double/triple of what is expected given the rest of the data).
# filtering for expected isi:
df_singlefile_30s = df_singlefile_30s[df_singlefile_30s.timeinterval_tonextpeak_inms < 100]

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))

# %% @ RT with glu-blockers and gabazine
# neuron_data.plot_rawdatatraces_with_cellattachedspikes('gabazineWashOn')
# manual count: 35 spikes/2s (skipping first 5 minutes) (total time 6.2 - 5 min.)
# data kinda messy but spikes still mostly picked up right in file #1
# neuron_data.plot_rawdatatraces_with_cellattachedspikes('GluBlockers_with_gabazine_0000')
# manual count: 34 spikes/2s initially, 27-35 spikes/2s later on (total time 20.5 min).
# not a gradual slow-down over the course of time, just more variance (slowdown mostly towards the middle of this recording file).

df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_with_GluBlockers_gabazineWashOn_0001.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx < (20000 * 30)]
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# looks like algorithm missed a handful of spikes (their isi's are double/triple of what is expected given the rest of the data).
# filtering for expected isi:
df_singlefile_30s = df_singlefile_30s[df_singlefile_30s.timeinterval_tonextpeak_inms < 100]

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))

# %% @ RT with glu-blockers and gabazine and quinpirole
neuron_data.plot_rawdatatraces_with_cellattachedspikes('gabazine_with_quinpirole_0')
# manual count: 38 spikes/2s (total time: 5.1 min) (washin file separate, skipped)
# S/N getting to be not great at all in VC, still, I'd say most spikes got picked up fine

df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_with_GluBlockers_with_gabazine_with_quinpirole_0002.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx < (20000 * 30)]
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# by now it may be two handfuls of spikes that weren't picked up; still looks more than OK to just filter:
df_singlefile_30s = df_singlefile_30s[df_singlefile_30s.timeinterval_tonextpeak_inms < 80]

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))

# %% @ RT with glu-blockers and other drugs washed off
neuron_data.plot_rawdatatraces_with_cellattachedspikes('drugsWashOut_0')
# manual count: 35-37 spikes/2s (total time: 17.4 min; basically count didn't change over the course of wash)

# S/N quite bad in VC recordings at this point, need to switch to looking at CC recordings.
# re-doing spike extraction on a 30s segment:
segment = neuron_data.blocks[11].segments[0].time_slice((670*pq.s), (700*pq.s))
spikes_dict = get_spikes_from_cellattachedrecording(segment, neuron_data.blocks[11].file_origin, 0,
                                                    getbaseline_lpfilter_freq=8,
                                                    detection_threshold=1,
                                                    plot='on')
df_singlefile_30s = pd.DataFrame(spikes_dict)
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# this looks about as neat as it gets

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))

# %% @ PT with glu-blockers and other drugs washed off
neuron_data.plot_rawdatatraces_with_cellattachedspikes('tempUp_0')
# manual count: 18 spikes/2s after ~2min.; cell actually goes quiet for a couple of minutes after that, then comes back on spiking kinda irregularly (~5 spikes/2s)
# (total time 7.8 min.)

# This really is a special case: cell is clearly spiking lustily at first, goes completely quiet for a while, then comes back with highly irregular spiking.
# The S/N on the final recording file is far from great, but having probed it I'm quite confident spikes did get extracted properly.
# grabbing the final 30s recorded in this condition:
df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_0003.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx > (4671019 - (20000 * 30))]  # starting from 30s before the final spike peak
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# I see one point that's an outlier at ~2.5s, all other isi's are between ~180 - 1250ms.

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))

# %% @ PT with glu-blockers and gabazine (washed on again)
neuron_data.plot_rawdatatraces_with_cellattachedspikes('tempUp_with_gabazine')
# manual count: 15 spikes/2s (total time: 8.5 min)

# grabbing the final 30s recorded in this condition:
df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_with_gabazine_0000.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx > (10205072 - (20000 * 30))]  # starting from 30s before the final spike peak
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# no outliers that are clearly points where a spike got skipped.

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))

# %% @ PT with glu-blockers and gabazine washed off again
neuron_data.plot_rawdatatraces_with_cellattachedspikes('tempUp_gabazineWashOut_0')
# 22.5 min. of recording; I'll take the last 30s
df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashOut_0000.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx > (27030217 - (20000 * 30))]  # starting from 30s before the final spike peak
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# values go between ~90 to 180ms, but they are spread pretty evenly and I see no outliers that are clearly points where a spike got skipped.

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))



# %% @ PT with glu-blockers and gabazine washed on again again
neuron_data.plot_rawdatatraces_with_cellattachedspikes('gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashInAgain_0000.abf')
# 11.4min. of recording; I'll take the last 30s
df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashInAgain_0000.abf']
df_singlefile_30s = df_singlefile[df_singlefile.spikepeak_idx > (13665852 - (20000 * 30))]  # starting from 30s before the final spike peak
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# evenly spread from ~55 - 73ms

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))


# %% @ PT with glu-blockers and gabazine washed off again again
neuron_data.plot_rawdatatraces_with_cellattachedspikes('gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashOutAgain_0000.abf')
# 24.8min. of recording; taking 30s towards the end (but not quite, as signal gets suddenly bad)
df_singlefile = cellattachedspikes_df[cellattachedspikes_df.file_origin == 'gapFree_with_GluBlockers_otherdrugsWashOut_tempUp_gabazineWashOutAgain_0000.abf']
time_window = ((df_singlefile.spikepeak_idx > (1250 * 20000)) & (df_singlefile.spikepeak_idx < (1280 * 20000)))
df_singlefile_30s = df_singlefile[time_window]
df_singlefile_30s.plot.scatter('timeinterval_tonextpeak_inms', 'peakamp_from_baseline')
# spread pretty evenly from ~100 to 220 ms; looks like it'd be a distribution with a relatively long tail but not outlier-y

singlefile_30s_isi_mean = df_singlefile_30s.timeinterval_tonextpeak_inms.mean()
singlefile_frequency = 1 / (singlefile_30s_isi_mean / 1000)
print('spiking frequency = ' + str(singlefile_frequency))
print('mean isi = ' + str(singlefile_30s_isi_mean))
singlefile_30s_isi_std = df_singlefile_30s.timeinterval_tonextpeak_inms.std()
print('std isi = ' + str(singlefile_30s_isi_std))
singlefile_30s_CoV = singlefile_30s_isi_std / singlefile_30s_isi_mean
print('CoV = ' + str(singlefile_30s_CoV))
