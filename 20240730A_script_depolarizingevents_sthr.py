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

neuron_name = '20240730A'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice seal (~1.5GOhm) and patch (@t=49.5s in gapFree_0000); cell spiking with freq. just over 20Hz
# and then held subthreshold at -60mV with -75pA DC. After drug application, cell stays at -60mV with -50pA DC.
# Seeing TONS of spontaneously occurring subthreshold depolarizations, some of them huge (up to ~20mV), and some of the time they seem rhythmic.

# %% getting depolarizing events - looking for good algorithm parameter settings
neuron_data.plot_eventdetecttraces_forsegment(0, 0, time_slice=[70, 100],
                                              noisefilter_hpfreq=5000,
                                              oscfilter_lpfreq=0.5,
                                              ttleffect_window=8,  # as seen in script_optoresponses: events all get picked up with peak posttl_t < 7ms.
                                              depol_to_peak_window=20,
                                              event_width_window=70,
                                              min_depolspeed=0.2,
                                              min_depolamp=1)
# min. depolspeed and amp chosen by eye based on noise-level in the recording - below these, it's really hard to tell whether events are really events
# filter freqs chosen by looking for settings that cause as little deformation to the raw data as possible while allowing for events to be picked up

# %% getting depolarizing events - applying algorithm to entire neuron recording
neuron_data.get_depolarizingevents_fromrawdata(noisefilter_hpfreq=5000,
                                              oscfilter_lpfreq=0.5,
                                              ttleffect_window=8,  # as seen in script_optoresponses: events all get picked up with peak posttl_t < 7ms.
                                              depol_to_peak_window=20,
                                              event_width_window=70,
                                              min_depolspeed=0.2,
                                              min_depolamp=1)

# plotting some traces to see how this generalized:
for block_idx in range(5, 14):
    neuron_data.plot_eventdetecttraces_forsegment(block_idx, 0)

# %% overview plots of depolarizing-events parameters
des_df = neuron_data.depolarizing_events
nbins = 100
# events parameter distributions
des_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', 'approx_oscinstphase', 'approx_oscslope'],
                                bins=nbins)
plt.suptitle('depolarizing events parameter distributions')

spont_events = ~des_df.applied_ttlpulse & (des_df.event_label.isna())
sizable_spont_events = spont_events & (des_df.amplitude > 5) & (des_df.amplitude < 50)
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
spont_sthr_events = (sizable_spont_events & unlabeled_events)

neuron_data.plot_depolevents(spont_sthr_events,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=30,
                                   plotwindow_inms = 100,
                                   plt_title='spontaneous APs')
