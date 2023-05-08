# %% imports
import os
import re
from singleneuron_class import SingleNeuron
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