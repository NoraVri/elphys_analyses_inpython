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
neuron_name = '20250401B2'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# looks like a pretty great recording, signal 400-600pA throughout; seeing funny-patterned amplitude modulation of the signal, too

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 1, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 2  # the first two blocks are tuning pulses/switches between VC and CC
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
# inst.freq ~10-14Hz and perhaps trending up a bit towards the end of these 5 min. of recording; but also took a detour to 14-16Hz for about 10s ~85s into this recording block
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0002.abf
# mean freq. = 11.961491203643645
# isi CoV = 0.09098933626512046

# %% recording condition: gabazine wash in
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
# perhaps a slight trend of increasing frequency, doesn't look at all significant though
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: gabazine applied
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
start_t_inms = 450000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=200,
                                                t_start_inms=start_t_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# from the inst.freq vs. time plot of the whole block, it looks like gabazine effect is only taking hold ~450s into this recording (~12.5min after switching to gabazine solution)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_0000.abf  - last ~100s only
# mean freq. = 18.289194257406784
# isi CoV = 0.1742285870353168

# %% recording condition: gabazine and quinpirole applied
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 101500
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                # detection_threshold=40,
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
# taking only the final part of the file, once holding level back to 0;
# still, freq. trending up and down over the course of this minute (starting ~22Hz, going down to ~16Hz and then back up).
# recording block gapFree_with_gabazine_with_quinpirole_0001.abf  - ~one minute at the end of this block
# mean freq. = 19.279108608992214
# isi CoV = 0.16141574210988757

# %% recording condition: drugs washout
block_idx = 3
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 290000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=300,
                                                tracelength_30s=False,
                                                t_start_inms=t_start_inms,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# freq. seems to be randomly going up and down throughout this block, perhaps a slight trend down though
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_drugsWashOut_0000.abf  - taking only the last ~30s
# mean freq. = 17.848344304445074
# isi CoV = 0.14903008841641557