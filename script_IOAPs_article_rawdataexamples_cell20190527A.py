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
vmin = -10
vmax = 100
tmin = 0
tmax = 18
dvdtmin = -4
dvdtmax = 13


neat_aps = aps_spont & neatevents
# to reduce the number of traces in the plot, take every 3rd AP
neat_aps_subset = snafs.keep_every_nth(neat_aps, n=3)
# plot APs
aps_axis, aps_dvdt_axis = singleneuron_data.plot_depolevents(neat_aps_subset,
                                   do_baselining=True,
                                 prealignpoint_window_inms=6,
                                 plotwindow_inms=18,
                                   # display_measures=True,
                                   )
# setting axes limits to be the same as for light-evoked APs panel
aps_axis.set_ylim([vmin, vmax])
aps_axis.set_xlim([tmin, tmax])
aps_dvdt_axis.set_ylim([dvdtmin, dvdtmax])
aps_dvdt_axis.set_xlim([vmin, vmax])
# adding boxes to mark zoom-in areas
xs = [3, 3, 5.5, 5.5, 3]
ys = [-1, 12, 12, -1, -1]
aps_axis.plot(xs, ys, color='red')

xs = [-2.5, -2.5, 12.5, 12.5, -2.5]
ys = [-0.1, 0.8, 0.8, -0.1, -0.1]
aps_dvdt_axis.plot(xs, ys, color='red')

# for inset: rescale axes
aps_axis.set_xlim([2, 6])  # same width as for light-evoked APs
aps_axis.set_ylim([-1, 12])
aps_dvdt_axis.set_xlim([-2.5, 12.5])
aps_dvdt_axis.set_ylim([-0.1, 0.8])


# %% panel 2 again, with ddvdt plotted as well
aps_axis, aps_dvdt_axis, aps_ddvdt_axis = singleneuron_data.plot_depolevents(neat_aps_subset,
                                   do_baselining=True,
                                 prealignpoint_window_inms=6,
                                 plotwindow_inms=18,
                                   plot_ddvdt=True,
                                   display_measures=True,
                                   )
# setting axes limits to be the same as for light-evoked APs panel
aps_axis.set_ylim([vmin, vmax])
aps_axis.set_xlim([tmin, tmax])
aps_dvdt_axis.set_ylim([dvdtmin, dvdtmax])
aps_dvdt_axis.set_xlim([vmin, vmax])
aps_ddvdt_axis.set_xlim([vmin, vmax])
# adding boxes to mark zoom-in areas
xs = [3, 3, 5.5, 5.5, 3]
ys = [-1, 12, 12, -1, -1]
aps_axis.plot(xs, ys, color='red')

xs = [-2.5, -2.5, 12.5, 12.5, -2.5]
ys = [-0.1, 0.8, 0.8, -0.1, -0.1]
aps_dvdt_axis.plot(xs, ys, color='red')

xs = [-2.5, -2.5, 12.5, 12.5, -2.5]
ys = [-0.1, 0.35, 0.35, -0.1, -0.1]
aps_ddvdt_axis.plot(xs, ys, color='red')

# for inset: rescale axes
aps_axis.set_xlim([2, 6])  # same width as for light-evoked APs
aps_axis.set_ylim([-1, 12])
aps_dvdt_axis.set_xlim([-2.5, 12.5])
aps_dvdt_axis.set_ylim([-0.1, 0.8])
aps_ddvdt_axis.set_xlim([-2.5, 12.5])
aps_ddvdt_axis.set_ylim([-0.1, 0.35])

# %% panel 4: light-evoked APs, aligned to TTL
# using only light-applied blocks that are included in neatevents
neatevents_blocks = des_df[neatevents].file_origin.unique()
neatevents_light_blocks = [block for block in neatevents_blocks if 'light' in block]
# plotting light-evoked APs, aligned to TTL onset
_, axes = singleneuron_data.plot_rawdatatraces_ttlaligned(*neatevents_light_blocks,
                                                colorby_measure='response_maxamp',
                                                color_lims=[80, 100],  # selects events to plot by amplitude; APs are 90-100mV
                                                prettl_t_inms=1,
                                                postttl_t_inms=25,
                                                plotdvdt=False
                                                )
aps_axis = axes[0]
# setting axes limits to be the same as for spont. APs panel
aps_axis.set_ylim([vmin, vmax])



# %% plotting light-evoked APs again, aligned to AP peak (and baselining to detected baseline-points, instead of to pre-TTL baseline)
neat_lightevoked_aps = aps & neatevents & ~spont_events
aps_axis, aps_dvdt_axis = singleneuron_data.plot_depolevents(neat_lightevoked_aps,
                                   do_baselining=True,
                                   prealignpoint_window_inms=9,
                                   plotwindow_inms=18,
                                   # display_measures=True,
                                   )
# setting axes limits to be the same as the other full-scale panels
aps_axis.set_ylim([vmin, vmax])
aps_axis.set_xlim([tmin, tmax])
aps_dvdt_axis.set_ylim([dvdtmin, dvdtmax])
aps_dvdt_axis.set_xlim([vmin, vmax])

# adding boxes to mark zoom-in areas
xs = [4.5, 4.5, 8.5, 8.5, 4.5]
ys = [-1, 12, 12, -1, -1]
aps_axis.plot(xs, ys, color='red')

xs = [-2.5, -2.5, 12.5, 12.5, -2.5]
ys = [-0.1, 0.8, 0.8, -0.1, -0.1]
aps_dvdt_axis.plot(xs, ys, color='red')

# for inset: rescale axes
# aps_axis.set_xlim([4.5, 8.5])
# aps_axis.set_ylim([-1, 12])
# aps_dvdt_axis.set_xlim([-2.5, 12.5])
# aps_dvdt_axis.set_ylim([-0.1, 0.8])

