# %% imports
from singleneuron_class import SingleNeuron
import singleneuron_analyses_functions as snafs
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# in this script: plots of raw data examples from the 'best typical' recording, cell 20190527A.

neuron_name = '20190527A'
singleneuron_data = SingleNeuron(neuron_name)
# see 20190527A_script_groupingdepolarizingevents for details on analyses and labeling of events
des_df = singleneuron_data.depolarizing_events
spont_events = ~des_df.applied_ttlpulse
aps = des_df.event_label == 'actionpotential'
aps_spont = aps & spont_events
fastevents = des_df.event_label == 'fastevent'  # 'fastevent' is our shorthand for fast subthreshold depolarizing event
neatevents = des_df.neat_event  # events from a 27.5min stretch of continuous recording during which conditions were particularly good and stable
# %% panel 1: 2min. trace of spontaneously ongoing activity, with APs and fastevents marked
figure, axes = singleneuron_data.plot_rawdatablocks('gapFree_0004', events_to_mark=(fastevents | aps_spont))
axes[0].set_xlim(720000, 840000)
# axes[0].set_ylim(-60, -40)  # same panel with different y-axis

# %% panel 2: spontaneous APs, aligned to peak
neat_aps = aps_spont & neatevents
# to reduce the number of traces in the plot, take every 3rd AP
neat_aps_subset = snafs.keep_every_nth(neat_aps, n=3)
# plot APs
aps_axis, aps_dvdt_axis = singleneuron_data.plot_depolevents(neat_aps_subset,
                                   colorby_measure='peakv_idx',  # have colorbar there so that same-scaled axes will actually be the same
                                   do_baselining=True,
                                   prealignpoint_window_inms=6,
                                   plotwindow_inms=19,
                                   )
# setting axes limits to be the same as for light-evoked APs panel
aps_axis.set_ylim([-1, 100])
aps_axis.set_xlim([-1, 19])
aps_dvdt_axis.set_ylim([-4, 12.5])
aps_dvdt_axis.set_xlim([-1, 100])
# adding boxes to mark zoom-in areas
xs = [0, 0, 5.5, 5.5, 0]
ys = [-.5, 11.5, 11.5, -.5, -.5]
aps_axis.plot(xs, ys, color='red')

xs = [-1, -1, 12, 12, -1]
ys = [-.15, .8, .8, -.15, -.15]
aps_dvdt_axis.plot(xs, ys, color='red')
# for inset: rescale axes
# aps_axis.set_xlim([0, 5.5])
# aps_axis.set_ylim([-0.5, 11.5])
# aps_dvdt_axis.set_ylim([-0.15, 0.8])
# aps_dvdt_axis.set_xlim([-1, 12])

# %% panel 3: prepotential amplitudes
aps_axis, aps_dvdt_axis, aps_ddvdt_axis = singleneuron_data.plot_depolevents(neat_aps_subset,
                                   do_baselining=True,
                                   prealignpoint_window_inms=3.5,
                                   plotwindow_inms=7,
                                   plot_ddvdt=True,
                                   display_measures=True,
                                   )
aps_axis.set_xlim([0, 7])
# rescale axes
# aps_axis.set_xlim([0, 3])
# aps_axis.set_ylim([-0.5, 11.5])
# aps_dvdt_axis.set_ylim([-0.15, 0.8])
# aps_dvdt_axis.set_xlim([-1, 12])
# aps_ddvdt_axis.set_xlim([-1, 12])
# aps_ddvdt_axis.set_ylim([-0.06, 0.2])

# %% panel 4: light-evoked APs
# using only light-applied blocks that are included in neatevents
neatevents_blocks = des_df[neatevents].file_origin.unique()
neatevents_light_blocks = [block for block in neatevents_blocks if 'light' in block]
# plotting light-evoked APs, aligned to TTL onset
_, axes = singleneuron_data.plot_rawdatatraces_ttlaligned(*neatevents_light_blocks,
                                                colorby_measure='response_maxamp',
                                                color_lims=[80, 100],  # selects events to plot by amplitude; APs are 90-100mV
                                                prettl_t_inms=1,
                                                postttl_t_inms=19,
                                                plotlims=[-1, 100, -4, 12.5]  # same as for spont.APs panel
                                                )
aps_axis = axes[0]
aps_dvdt_axis = axes[1]
# setting axes limits to be the same as for spont. APs panel
aps_axis.set_ylim([-1, 100])
aps_axis.set_xlim([-1, 19])
aps_dvdt_axis.set_ylim([-4, 12.5])
aps_dvdt_axis.set_xlim([-1, 100])
# adding boxes to mark zoom-in areas
xs = [5.5, 5.5, 11, 11, 5.5]
ys = [0, 13, 13, 0, 0]
aps_axis.plot(xs, ys, color='red')

xs = [0, 0, 13, 13, 0]
ys = [-.15, .8, .8, -.15, -.15]
aps_dvdt_axis.plot(xs, ys, color='red')
# for inset: rescale axes
# aps_axis.set_xlim([5.5, 11])
# aps_axis.set_ylim([0, 12])
# aps_dvdt_axis.set_ylim([-0.15, 0.8])
# aps_dvdt_axis.set_xlim([0, 13])

# %% plotting light-evoked APs again, aligned to AP peak (and baselining to detected baseline-points, instead of to pre-TTL baseline)
neat_lightevoked_aps = aps & neatevents & ~spont_events
aps_axis, aps_dvdt_axis = singleneuron_data.plot_depolevents(neat_lightevoked_aps,
                                   colorby_measure='peakv_idx',  # have colorbar there so that same-scaled axes will actually be the same
                                   do_baselining=True,
                                   prealignpoint_window_inms=6,
                                   plotwindow_inms=19,
                                   )
# setting axes limits to be the same as the other full-scale panels
aps_axis.set_ylim([-1, 100])
aps_axis.set_xlim([-1, 19])
aps_dvdt_axis.set_ylim([-4, 12.5])
aps_dvdt_axis.set_xlim([-1, 100])

# adding boxes to mark zoom-in areas
xs = [0, 0, 5.5, 5.5, 0]
ys = [-.5, 11.5, 11.5, -.5, -.5]
aps_axis.plot(xs, ys, color='red')

xs = [-1, -1, 12, 12, -1]
ys = [-.15, .8, .8, -.15, -.15]
aps_dvdt_axis.plot(xs, ys, color='red')

# for inset: rescale axes
aps_axis.set_xlim([0, 5.5])
aps_axis.set_ylim([-0.5, 11.5])
aps_dvdt_axis.set_ylim([-0.15, 0.8])
aps_dvdt_axis.set_xlim([-1, 12])

