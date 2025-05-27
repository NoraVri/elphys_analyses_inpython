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
neuron_name = '20250401D1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# S/N not great especially in VC recordings, but overall looks like there should be enough good data for analysis

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 2
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
# mostly very steady freq. ~6Hz
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0002.abf
# mean freq. = 6.462767243040441
# isi CoV = 0.09485001045265956

block_idx = 3
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 155400  # cutting off switch to VC mode
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.7,
                                                tracelength_30s=False,
                                                getbaseline_lpfilter_freq=5,
                                                t_end_inms=t_end_inms,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0003.abf
# mean freq. = 6.736176951553777
# isi CoV = 0.1772559705231886

block_idx = 4
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
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0004.abf
# mean freq. = 6.800563180838309
# isi CoV = 0.13401662960394592

block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.5,
                                                tracelength_30s=False,
                                                getbaseline_lpfilter_freq=5,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#  frequency becoming more variable overall, while also increasing on average
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0005.abf
# mean freq. = 7.392278601935308
# isi CoV = 0.1545456005527785

block_idx = 6
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.7,
                                                tracelength_30s=False,
                                                getbaseline_lpfilter_freq=10,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0006.abf
# mean freq. = 7.595154335059472
# isi CoV = 0.12712917691478218

# overall, it looks like spike frequency went up by 1Hz, from ~6.5 to 7.5, since the start of recording (~7 minutes)

# %% recording condition: gabazine wash in
block_idx = 10
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 72000  # in between two episodes where baselineV too unstable for easy and accurate spike extraction
t_end_inms = 239000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.8,
                                                tracelength_30s=False,
                                                t_start_inms=t_start_inms,
                                                t_end_inms=t_end_inms,
                                                getbaseline_lpfilter_freq=10,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# seems like if the neuron is changing its frequency at all, it's doing so in jumps (up and down)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: gabazine applied
block_idx = 11
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 62000  # after this, baselineV too unstable for easy and accurate spike extraction
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.8,
                                                tracelength_30s=False,
                                                t_end_inms=t_end_inms,
                                                getbaseline_lpfilter_freq=10,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_0000.abf
# mean freq. = 8.132219170611036
# isi CoV = 0.0982240449380012

# %% recording condition: gabazine applied, quinpirole wash in
block_idx = 14
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.8,
                                                tracelength_30s=False,
                                                getbaseline_lpfilter_freq=10,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# doesn't really look like there's a trend up; if anything, a trend down...
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: gabazine and quinpirole applied
block_idx = 15
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 192000  # cutting off switch to VC
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=1.2,
                                                tracelength_30s=False,
                                                t_end_inms=t_end_inms,
                                                getbaseline_lpfilter_freq=10,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_with_quinpirole_0000.abf
# mean freq. = 8.881409197499751
# isi CoV = 0.07233330063849765

block_idx = 16
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=50,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# from the start of this recording to the end (5 minutes), there's a trend down by ~1Hz (11 down to 10)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_with_quinpirole_0001.abf
# mean freq. = 9.822979048499821
# isi CoV = 0.07267799989750291

# %% recording condition: drugs washout
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 1000000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=50,
                                                t_start_inms=t_start_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# that's 20 minutes worth of recording while washing; no significant change in frequency at all.
# Same seemed to be true in the other 3 minutes' worth of washout recording.
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_drugsWashOut_0000.abf
# mean freq. = 9.846398276410158
# isi CoV = 0.07284272378464986

