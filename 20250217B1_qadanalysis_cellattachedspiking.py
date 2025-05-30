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
neuron_name = '20250217B1'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.plot_rawdatablocks()

# notes on raw data:
# doesn't look like the greatest recording: signal amplitude only ~50pA (if at all), hard to tell if neuron is actually quiet sometimes or signal just too low

# raw data cleanups
# removing recording channel not belonging to this neuron:
# blocknameslist = neuron_data.get_blocknames(printing='off')
# for blockname in blocknameslist:
#     neuron_data.rawdata_remove_nonrecordingchannel(blockname, 2, pairedrecording=True)
# neuron_data.write_results()

# %% going over data by recording condition
# %% recording condition: baseline @ RT
block_idx = 1
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
#
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_0001.abf
# mean freq. = 9.312198890030789
# isi CoV = 0.306922395801286
# not using the first recording block: looks like the only spikes in there are during tuning pulses

# %% recording condition: quinpirole wash in
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
# qiute the handful of noise-things, I don't see any real change in freq though
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: quinpirole applied
block_idx = 5
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
end_t_inms = 150000
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=20,
                                                getnoise_hpfilterfreq=800,
                                                getbaseline_lpfilter_freq=3,
                                                t_end_inms=end_t_inms,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# the frequency profile looks very different for the first 150s (pretty regular ~12Hz) and the rest of this file (super irregular, 4-40Hz)
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_quinpirole_0000.abf  - full recording block
# mean freq. = 10.198988046831126
# isi CoV = 0.4227620896425558
# recording block gapFree_quinpirole_0000.abf - first 150s
# mean freq. = 10.083863014393879
# isi CoV = 0.19985904875268914

# %% recording condition: quinpirole applied, gabazine wash in
block_idx = 6
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=20,
                                                getnoise_hpfilterfreq=800,
                                                getbaseline_lpfilter_freq=3,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# looks like spiking freq increases in waves right around when gabazine getting to the bath; but it's mostly calmed back down by the end of these 5 minutes
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))

# %% recording condition: quinpirole and gabazine applied
block_idx = 7
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=20,
                                                getnoise_hpfilterfreq=800,
                                                getbaseline_lpfilter_freq=3,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# looks like baseline spiking is ~8Hz but with lots of excursions up
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))
# recording block gapFree_quinpirole_gabazine_0000.abf
# mean freq. = 9.774804081049464
# isi CoV = 0.40201510994030903

# %% recording condition: drugs wash out
block_idx = 2
segment = neuron_data.blocks[block_idx].segments[0]
segment_file_origin = neuron_data.blocks[block_idx].file_origin
results = get_spikes_from_cellattachedrecording(segment, segment_file_origin, 0,
                                                detection_threshold=20,
                                                getnoise_hpfilterfreq=800,
                                                getbaseline_lpfilter_freq=3,
                                                tracelength_30s=False,
                                                plot='on')
qad_scatter_isis_fromdict(results[0])
plt.title(segment.file_origin)
spikes_df = pd.DataFrame(results[0])
plot_cellattachedspikes_instantaneous_frequency(spikes_df, 20000)
# cell stops spiking pretty abruptly after ~5min. of wash.
print('recording block ' + segment.file_origin)
print('mean freq. = ' + str(results[2]))
print('isi CoV = ' + str(results[3]))