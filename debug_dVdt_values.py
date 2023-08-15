# %% imports
import os
import re
from singleneuron_class import SingleNeuron
import singleneuron_analyses_functions as snafs
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from singleneuron_analyses_functions import make_derivative_per_ms
# %%
neuron_name = '20201125B'
singleneuron_data = SingleNeuron(neuron_name)
des_df = singleneuron_data.depolarizing_events
# %%
example_segment = singleneuron_data.blocks[4].segments[0]
example_voltage_trace = example_segment.analogsignals[0]

time_axis = example_voltage_trace.times
time_axis = time_axis.rescale('ms').magnitude
sampling_period_inms = example_voltage_trace.sampling_period.rescale('ms')
ms_insamples = int(1 / (sampling_period_inms))

voltage_recording = np.array(np.squeeze(example_voltage_trace))
npdiff_voltage_recording = np.diff(voltage_recording)
npdiff_timestepadjusted = npdiff_voltage_recording / sampling_period_inms
# npgradient_voltage_recording = np.gradient(voltage_recording, ms_insamples)
permsdiff_voltage_recording = make_derivative_per_ms(voltage_recording, ms_insamples)

plt.figure()
plt.plot(time_axis, voltage_recording, label='voltage recording')
plt.plot(time_axis[:len(npdiff_voltage_recording)], npdiff_voltage_recording, label='np diff')
plt.plot(time_axis[:len(npdiff_voltage_recording)], npdiff_timestepadjusted, label='np diff adjusted for timestep')
# plt.plot(time_axis, npgradient_voltage_recording, label='np gradient')
plt.plot(time_axis[:len(permsdiff_voltage_recording)], permsdiff_voltage_recording, label='per ms diff')
plt.legend()

# %%
spont_events = ~des_df.applied_ttlpulse
aps = des_df.event_label == 'actionpotential'
aps_spont = aps & spont_events
fastevents = des_df.event_label == 'fastevent'
neatevents = des_df.neat_event
neat_spontaps = (aps_spont & neatevents)

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



# %% TODO following fixes:
# - check that events are being properly picked up for multiple neurons; especially APs and currentpulsechanges
# - re-do singleneuron analyses for all neurons in the depolarizingevents-dataset(s)