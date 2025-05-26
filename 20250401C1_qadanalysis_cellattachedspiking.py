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
neuron_name = '20250401C1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# not the greatest recording in terms of S/N; still, should be easy enough to extract spikes for most recording conditions

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 4  # the first couple of blocks are tuning pulses/VC-CCswitches
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_start_inms = 5000  # after tuning pulses turned off
t_end_inms = 180000  # after this, baseline trends become too unstable for easy and accurate spike extraction
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.5,
                                                tracelength_30s=False,
                                                t_start_inms=t_start_inms,
                                                t_end_inms=t_end_inms,
                                                getbaseline_lpfilter_freq=10,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# in these 175s of baseline recording, around 60s in there's a slight increase, then decrease in frequency (though looks like by just 1-2Hz); calculated number reflects grand average
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0004.abf
# mean freq. = 17.205708314052224
# isi CoV = 0.10551172466236083

# %% recording condition: gabazine applied @ RT
block_idx = 23
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
# small handful of noise-things in there, doesn't feel worth going after
# freq seems to take another little jump up at ~200s into this block; it's only by ~1Hz though, really quite subtle. Number calculated as grand average for the entire recording block
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_wtih_gabazine_0001.abf
# mean freq. = 19.472819775716705
# isi CoV = 0.10334232635120803

# %% recording condition: "gabazine overload" (dose of gabazine directly to bath, twice)
block_idx = 18
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
# nothing unusual to be seen here, it might as well be a baseline recording
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_wtih_gabazineOverload_0000.abf
# mean freq. = 19.203421661112255
# isi CoV = 0.1100374806588842

block_idx = 21
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
# just as previous, nothing unusual to be seen here; firing rate down again just a tad compared to the other recording in the same condition
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_wtih_gabazineOverload_0003.abf
# mean freq. = 18.50739754506285
# isi CoV = 0.14924142594748255



# %% recording condition: gabazine and quinpirole applied
block_idx = 15
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
t_end_inms = 154000  # cutting off switch to VC
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=0.7,
                                                getbaseline_lpfilter_freq=10,
                                                t_end_inms=t_end_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# the usual handful of noise-things, otherwise this freq-over-time curve is about as flat as I've ever seen them
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_with_gabazine_with_quinpirole_0000.abf
# mean freq. = 17.080851312749218
# isi CoV = 0.12890854602030244

## after this, signal/noise starting to be too low for easy and accurate spike detection
