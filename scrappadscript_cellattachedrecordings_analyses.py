# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

from detecta import detect_peaks
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
from singleneuron_analyses_functions import make_cellattachedspikepeaks_dictionary

# %% scrappad analysis of spiking frequency in 20250401 recordings
# %% importing the data
# neuron_name = '20250401A1'
# neuron_name = '20250401A2'
neuron_name = '20250401B1'
# neuron_name = '20250401B2'
# neuron_name = '20250401C1'
# neuron_name = '20250401C2'
# neuron_name = '20250401D1'
# neuron_name = '20250401D2'

# getting cell-attached spikes, in a df sorted by file timestamp
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_spikes_fromcellattachedrecording()
cellattachedspikes_df = neuron_data.cellattachedspikes.copy()
file_order = list(neuron_data.recordingblocks_index.file_origin)
sorted_df = cellattachedspikes_df.sort_values(by="file_origin", key=lambda x:x.map(file_order.index))
# plotting an overview of the data (time interval between spikepeaks, by recording file)
sns.boxplot(sorted_df, x="file_origin", y="timeinterval_tonextpeak_inms")
plt.xticks(rotation=80)
plt.show()
plt.tight_layout(pad=1)


plt.figure()
sns.stripplot(sorted_df, x="file_origin", y="timeinterval_tonextpeak_inms")
sns.violinplot(sorted_df, x="file_origin", y="timeinterval_tonextpeak_inms")
plt.xticks(rotation=80)
plt.show()
plt.tight_layout(pad=1)


# %% notes
# 20250401A1: according to plots, may be speeding up with each drug - LOTs of larger ISIs get categorized as outliers.











# %%
neuron_data.get_recordingblocks_index()
sampling_freq = float(neuron_data.recordingblocks_index.sampling_freq_inHz.unique())
blocks_to_plot = list(neuron_data.recordingblocks_index.file_origin[neuron_data.recordingblocks_index.t_recorded_ins > 30])

# neuron_data.plot_rawdatatraces_with_cellattachedspikes(blocks_to_plot)

baseline_recblock = 'gapFree_0003.abf'
baseline_recblock_df = cellattachedspikes_df[cellattachedspikes_df.file_origin == baseline_recblock]
baseline_t_start = 100
baseline_t_end = 200
tsnippet_baseline_recblock_df = baseline_recblock_df[((baseline_recblock_df.spikepeak_idx > (sampling_freq * baseline_t_start)) & (baseline_recblock_df.spikepeak_idx < (sampling_freq * baseline_t_end)))]



drug_gabazine_recblock = 'gapFree_with_gabazine_0000.abf'
drug_gabazine_t_start = 100
drug_gabazine_t_end = 200







# %% importing some data
cell20250217A1 = SingleNeuron('20250217A1')
cell20250217A1.get_spikes_fromcellattachedrecording(plot='off')
cell20250217A1_spikes_df = cell20250217A1.cellattachedspikes
cell20250217A1.plot_rawdatatraces_with_cellattachedspikes()
# %%

cell20250217B2 = SingleNeuron('20250217B2')
cell20250217C1 = SingleNeuron('20250217C1')
cell230608A = SingleNeuron('230608A')
# getting spikes
cell20250217B2_spikes_df = cell20250217B2.get_spikes_fromcellattachedrecording()
cell20250217C1_spikes_df = cell20250217C1.get_spikes_fromcellattachedrecording()
cell230608A_spikes_df = cell230608A.get_spikes_fromcellattachedrecording()





# %%





recording_segment = cell20250217A1.blocks[3].segments[0]
# sampling_frequency = float(recording_segment.analogsignals[0].sampling_rate.rescale('Hz'))
# recording_segment_datatrace = recording_segment.analogsignals[0].squeeze()
#
# plt.plot(recording_segment_datatrace)
#
# data_trace_lpfiltered, data_trace_hpfiltered = apply_filters_to_vtrace(recording_segment_datatrace,
#                                                                        0.5,
#                                                                        5000,
#                                                                        sampling_frequency,
#                                                                        plot='off')
#
# eventdetect_trace = np.array(recording_segment_datatrace) - data_trace_lpfiltered - data_trace_hpfiltered

spikes_dict, data_trace_pastthreshold_idcs = get_spikes_from_cellattachedrecording(recording_segment, 'file', 0,
                                   plot='off')

# single_segment = recording_segment
# recording_primary = single_segment.analogsignals[0]
# recording_secondary = single_segment.analogsignals[1]
# time_axis = recording_primary.times
# sampling_frequency = float(recording_primary.sampling_rate.rescale('Hz'))  # cast to float gets rid of quantities
#
# primary_recording_unit = str(recording_primary.units)[-2:]
# data_trace = recording_primary.squeeze()
# empty_dict = make_cellattachedspikepeaks_dictionary()
# for block in cell20250217B2.blocks:
#     for i, segment in enumerate(block.segments):
#         dict = get_spikes_from_cellattachedrecording(segment, block.file_origin, i,
#                                                      plot='off')
#         for key in empty_dict:
#             empty_dict[key] += list(dict[key])
