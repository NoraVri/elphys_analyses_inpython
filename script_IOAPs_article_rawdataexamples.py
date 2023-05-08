# %% imports
from singleneuron_class import SingleNeuron
import singleneuron_analyses_functions as snafs
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np


neuron_name = '20201125B'
singleneuron_data = SingleNeuron(neuron_name)
des_df = singleneuron_data.depolarizing_events
spont_events = ~des_df.applied_ttlpulse
aps = des_df.event_label == 'actionpotential'
aps_spont = aps & spont_events
fastevents = des_df.event_label == 'fastevent'
neatevents = des_df.neat_event
neat_spontaps = (aps_spont & neatevents)


# %% panel 2 again, with ddvdt plotted as well
vmin = -10
vmax = 100
tmin = 0
tmax = 18
dvdtmin = -4
dvdtmax = 13

neat_aps = aps_spont & neatevents
# to reduce the number of traces in the plot and find a good subset to show
neat_aps_subset = snafs.keep_every_nth(neat_aps, n=22, start_idx=4)


aps_axis, aps_dvdt_axis, aps_ddvdt_axis = singleneuron_data.plot_depolevents(neat_aps_subset,
                                   do_baselining=True,
                                 prealignpoint_window_inms=6,
                                 plotwindow_inms=15,
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
ys = [-0.5, 15, 15, -0.5, -0.5]
aps_axis.plot(xs, ys, color='red')

xs = [-0.5, -0.5, 15, 15, -0.5]
ys = [-0.05, 1, 1, -0.05, -0.05]
aps_dvdt_axis.plot(xs, ys, color='red')

xs = [-1.5, -1.5, 13.5, 13.5, -1.5]
ys = [-0.1, 0.35, 0.35, -0.1, -0.1]
aps_ddvdt_axis.plot(xs, ys, color='red')

# for inset: rescale axes
# aps_axis.set_xlim([3, 5.5])  # same width as for light-evoked APs
# aps_axis.set_ylim([-0.5, 15])
# aps_dvdt_axis.set_xlim([-0.5, 15])
# aps_dvdt_axis.set_ylim([-0.05, 1])
# aps_ddvdt_axis.set_xlim([-1.5, 13.5])
# aps_ddvdt_axis.set_ylim([-0.1, 0.35])

# plotting prepotential-APs separately, to mark them in different color in the figure panels
neat_aps_withprepotential_subset = (neat_aps_subset & (~des_df.ap_prepotential_amp.isna()))
aps_axis, aps_dvdt_axis, aps_ddvdt_axis = singleneuron_data.plot_depolevents(neat_aps_withprepotential_subset,
                                   do_baselining=True,
                                 prealignpoint_window_inms=6,
                                 plotwindow_inms=15,
                                   plot_ddvdt=True,
                                   display_measures=True,
                                   )
# setting axes limits to be the same
aps_axis.set_ylim([vmin, vmax])
aps_axis.set_xlim([tmin, tmax])
aps_dvdt_axis.set_ylim([dvdtmin, dvdtmax])
aps_dvdt_axis.set_xlim([vmin, vmax])
aps_ddvdt_axis.set_xlim([vmin, vmax])
# for inset: rescale axes
# aps_axis.set_xlim([3, 5.5])  # same width as for light-evoked APs
# aps_axis.set_ylim([-0.5, 15])
# aps_dvdt_axis.set_xlim([-0.5, 15])
# aps_dvdt_axis.set_ylim([-0.05, 1])
# aps_ddvdt_axis.set_xlim([-1.5, 13.5])
# aps_ddvdt_axis.set_ylim([-0.1, 0.35])