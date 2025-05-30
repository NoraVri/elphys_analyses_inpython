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
neuron_name = '20250217B2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# looks like a very nice recording, signal amplitude >200pA throughout
# can see spiking freq go through phases of speeding up and slowing down with the naked eye

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 0
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
start_t_inms = 8000  # cutting off tuning pulses
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                t_start_inms=start_t_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0000.abf
# mean freq. = 4.551975122031059
# isi CoV = 0.21893280069861032

block_idx = 1
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0001.abf
# mean freq. = 9.843613214037424
# isi CoV = 0.24558462374127044

# There's about 5 minutes between the end of block 0 and the start of block 1.
# Spiking freq makes a quick detour up to ~10Hz after about 2 min. of recording in block 0,
# so I easily believe that spiking freq increased overall over the course of time

# %% recording condition: quinpirole wash in
block_idx = 4
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# that looks like a decided reduction in spiking freq ~140s into this block (right as quinpirole starting to get to the bath)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: quinpirole applied
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# looks like frequency goes up and down in waves that last ~50s (mean ~8Hz, until it takes a detour up to ~30Hz for a few s)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_quinpirole_0000.abf
# mean freq. = 7.887995974990162
# isi CoV = 0.1998969187134379

# %% recording condition: quinpirole applied, gabazine wash in
block_idx = 6
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# that sure looks like something is happening to spiking freq, it starts to make pretty crazy waves up and down starting ~160s into this block
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: quinpirole and gabazine applied
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# if I were picking just 30s of this to get numbers from, mean freq. could be anywhere between 4 and 10Hz based on this recording
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_quinpirole_gabazine_0000.abf
# mean freq. = 6.640940476064335
# isi CoV = 0.3078386192291933

# %% recording condition: drugs wash out
block_idx = 2
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# after ~7min. of washing, neuron starts to do pauses in firing for seconds at the time
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))


block_idx = 3
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_drugsWashOut_0001.abf
# mean freq. = 5.539528372563317
# isi CoV = 1.0205403135898612