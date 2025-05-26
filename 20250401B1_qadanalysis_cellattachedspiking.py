# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_analyses_functions import get_spikes_from_cellattachedrecording
from singleneuron_plotting_functions import qad_scatter_isis_fromdict
from singleneuron_plotting_functions import plot_cellattachedspikes_instantaneous_frequency
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
import os
import re
import json

# quick-and-dirty analysis steps:
# import data, cleanup where necessary (i.e., remove channels not belonging to neuron and/or any any sections recorded in the wrong mode)
# identify unique recording conditions (temperature, drug) and collect all files per condition
# per condition, pick a 30s trace to get numbers from and (manually) place these in excel table

## importing the data
neuron_name = '20250401B1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# signal amplitude not great (up to ~150pA, usually more like 50-100pA) and by eye it looks like S/N ratio may get problematic for spike extraction.

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 2  # the first two blocks are tuning pulses/switches between VC and CC
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# clearly there are a couple of noise-things in here; too little to bother with correcting right now
# inst.freq 16-20Hz, no clearly visible trends up or down.
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0002.abf
# mean freq. = 18.078979568473393
# isi CoV = 0.07630648801042438

# %% recording condition: gabazine wash in
block_idx = 4
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# a small few noise-things in here, too; too little to bother with
# inst.freq 16-20Hz initially, trending up (18-22Hz after ~5min) starting before gabazine could have properly reached the bath (usually ~150s into recording block)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: gabazine applied
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=40,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# a small few noise-things in here, too; too little to bother with
# inst.freq ~22-26Hz initially, but trending down reaching 16-24Hz after ~200s.
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_0000.abf
# mean freq. = 20.62448700764818
# isi CoV = 0.0799674434494461

# %% recording condition: gabazine and quinpirole applied
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 97400
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=40,
                                                t_start_inms=t_start_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# a small few noise-things in here, too; too little to bother with
# this file was recorded at least 5 min. after adding quinpirole; frequency changes (between 20-100s in this file
# freq. is 17-21Hz; otherwise, 20-24Hz) are due to changing holding level (from 0mV down to -70mV).
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_with_quinpirole_0001.abf
# mean freq. = 21.85479543073267  - in the final part of the file, once holding level back to 0
# isi CoV = 0.06938223354674976

# %% recording condition: drugs washout
# block_idx = 3
# segment = neuron_data.blocks[block_idx].segments[0]
# segment_file_origin = neuron_data.blocks[block_idx].file_origin
# results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
#                                                 tracelength_30s=False,
#                                                 plot='on')
# qad_scatter_isis_fromdict(results[0])
# plt.title(segment.file_origin)
# spikes_df = pd.DataFrame(results[0])
# plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# #
# print('recording block ' + segment.file_origin)
# print('mean freq. = ' + str(results[2]))
# print('isi CoV = ' + str(results[3]))

# only 5 minutes of recording, and no clear trends in frequency:
# I'm not gonna bother with this one, doesn't look like washout took effect at all.
