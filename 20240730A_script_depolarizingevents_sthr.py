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

# # %% getting depolarizing events - looking for good algorithm parameter settings
# neuron_data.plot_eventdetecttraces_forsegment(0, 0, time_slice=[70, 100],
#                                               noisefilter_hpfreq=6000,
#                                               oscfilter_lpfreq=0.5,
#                                               ttleffect_window=8,  # as seen in script_optoresponses: events all get picked up with peak posttl_t < 7ms.
#                                               depol_to_peak_window=20,
#                                               event_width_window=70,
#                                               min_depolspeed=0.5,
#                                               min_depolamp=1)
# # min. depolspeed and amp chosen by eye based on noise-level in the recording - below these, it's really hard to tell whether events are really events
# # filter freqs chosen by looking for settings that cause as little deformation to the raw data as possible while allowing for events to be picked up
#
# # %% getting depolarizing events - applying algorithm to entire neuron recording
# neuron_data.get_depolarizingevents_fromrawdata(noisefilter_hpfreq=5000,
#                                               oscfilter_lpfreq=0.5,
#                                               ttleffect_window=8,  # as seen in script_optoresponses: events all get picked up with peak posttl_t < 7ms.
#                                               depol_to_peak_window=20,
#                                               event_width_window=70,
#                                               min_depolspeed=0.5,
#                                               min_depolamp=1)
#
# # plotting some traces to see how this generalized:
# for block_idx in range(5, 14):
#     neuron_data.plot_eventdetecttraces_forsegment(block_idx, 0)

# %% exploration of depolarizing-events parameters
des_df = neuron_data.depolarizing_events
nbins = 100
# events parameter distributions
des_df.hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', ],
                                bins=nbins)
plt.suptitle('depolarizing events parameter distributions')
# that sure looks far from perfect - for example, quite a number of events got picked up as having baselineV > -10mV.
highbaselinev_events = des_df.baselinev > -10
neuron_data.plot_depolevents(highbaselinev_events,
                             prealignpoint_window_inms=100,
                             plotwindow_inms=200)
# of course - Gseal formation. The first real AP after break-in occurs just after 49500ms into GapFree_0000.
# Labeling all events that came before as seal formation:
sealformation_events = ((des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx < (49500*20000)))
des_df.loc[sealformation_events, 'event_label'] = 'Gsealformation_event'

# Also, let's stick to spont.events, and limit ourselves to APs and other unlabeled events:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events_spont = des_df.event_label.isna() & spont_events
aps_spont = (des_df.event_label == 'actionpotential') & spont_events

des_df[aps_spont].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', ],
                       bins=nbins)
plt.suptitle('automatically labeled APs')

des_df[unlabeled_events_spont].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', ],
                       bins=nbins)
plt.suptitle('spont.events')
# Still not looking perfect - there's quite a number of things labeled actionpotential with too long a rise time for that,
# and the spont.events parameter distributions suggest that there's still some stray APs in there.

longrt_aps = aps_spont & (des_df.rise_time_20_80 > 0.4)  # there's a pretty steep drop in the histogram there
neuron_data.plot_depolevents(longrt_aps,
                             do_baselining=True,
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=100,
                             plotwindow_inms=200)
plt.title('long rt APs')
shortrt_aps = aps_spont & (des_df.rise_time_20_80 < 0.4)  # there's a pretty steep drop in the histogram there
neuron_data.plot_depolevents(shortrt_aps,
                             do_baselining=True,
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=100,
                             plotwindow_inms=200)
plt.title('short rt APs')
# No doubt that these plots look somewhat different, but they are definitely all APs. Peaks are properly picked up,
# I think the differences in measurement come down to where the baseline-point was put.
# Makes sense, my code never was meant to handle neurons that don't sit at a baselineV but spike continuously....

# Let's move on and see the unlabeled events:

des_df[unlabeled_events_spont].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', ],
                       bins=nbins)
plt.suptitle('spont.events')
des_df[unlabeled_events_spont].plot.scatter('rise_time_20_80', 'amplitude',
                                            c='baselinev', colormap='Spectral')
plt.suptitle('spont.events')

# clear divide by amplitude: events are either <20mV or >40. Let's first see the larger ones:
possibly_aps = unlabeled_events_spont & (des_df.amplitude > 30)
neuron_data.plot_depolevents(possibly_aps,
                             do_baselining=True,
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=100,
                             plotwindow_inms=200)
# yes, these are definitely all APs. Labeling them as such:
des_df.loc[possibly_aps, 'event_label'] = 'actionpotential'
unlabeled_events_spont = des_df.event_label.isna() & spont_events
aps_spont = (des_df.event_label == 'actionpotential') & spont_events

des_df[unlabeled_events_spont].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude',
                                'baselinev', ],
                       bins=nbins)
plt.suptitle('spont.events')
des_df[unlabeled_events_spont].plot.scatter('rise_time_20_80', 'amplitude',
                                            c='baselinev', colormap='Spectral')
plt.suptitle('spont.events')

# %%
large_unlabeled_events_spont = (des_df.amplitude > 10) & unlabeled_events_spont
inquinpirole_events = (des_df.file_origin.str.contains('uinpi'))
drugfree_events = ~inquinpirole_events
neuron_data.plot_depolevents((large_unlabeled_events_spont & inquinpirole_events),
                             do_baselining=True,
                             plot_dvdt=False,
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=30,
                             plotwindow_inms=125,
                             plt_title='events with drug')
neuron_data.plot_depolevents((large_unlabeled_events_spont & drugfree_events),
                             do_baselining=True,
                             plot_dvdt=False,
                             colorby_measure='baselinev',
                             prealignpoint_window_inms=30,
                             plotwindow_inms=125,
                             plt_title='no drug')
