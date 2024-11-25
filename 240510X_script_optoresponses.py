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

neuron_name = '240510X'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks like a neat enough recording at first glance: cell held with ~-200pA to keep -75mV; and light responses
# look like they are mostly subthreshold. Definitely some APs in the first recording file, during which neuron is
# clearly all sorts of spontaneously active... In general, big difference between the first recording file (baseline)
# and the rest of recordings.

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=20)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# From here, it looks like the four recording files in the middle were taken under the same conditions; whereas the cell
# looks to have been significantly less leaky during the first, and more leaky during the final recording file

# Let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Not entirely sure what I'm looking at: seems APs may have amplitudes of 1 - 2.5nA;
# but also subthreshold responses can go up to ~600pA.
# Peak times are also messed up: most are picked up as <8ms, but there are a handful that got picked up as being
# >25ms post ttl onset. Let's see them:
neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms > 20],
                            postttl_t_inms=25,
                            prettl_t_inms=5,
                            )
# That's all spontaneous activity getting marked as response.
## Re-running get_singlepulse_ttlonmeasures_fromrawdata with 20ms window
# Now we have a couple of points that got measured as having their peak <2ms post ttl; I'll bet these are mismeasured
# Also, if there was any distinction between APs and subthreshold responses by amplitude, it's even less clear now.
# %%
neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 450],
                            postttl_t_inms=30,
                            prettl_t_inms=10,
                            )

block1_ttlonmeasures = ttlonmeasures[ttlonmeasures.file_origin == '2024_05_10_0000.abf']
neuron_data.plot_ttlaligned(block1_ttlonmeasures,
                            postttl_t_inms=30,
                            prettl_t_inms=10,
                            )
# lots of APs and/or dendritic spiking;
# also definitely some traces where no stim was applied (box does fail sometimes at stim.duration 0.25ms);
# also for subthreshold responses, not sure if response is compound or just overlaid on ongoing activity

neuron_data.plot_ttlaligned(ttlonmeasures[~(ttlonmeasures.file_origin == '2024_05_10_0000.abf')],
                            postttl_t_inms=30,
                            prettl_t_inms=10,
                            )
