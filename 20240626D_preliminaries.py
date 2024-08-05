# %% imports
from singleneuron_class import SingleNeuron
from singleneuron_plotting_functions import plot_ttlaligned
import singleneuron_analyses_functions as snafs
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %%
neuron_name = '20240626D'
# sulpiride applied
# spont.activity, longPulses and optoStim, with and without Sulpiride; also shortPulse with Sulpiride


singleneuron_data = SingleNeuron(neuron_name)


# %% figuring out a figure of averaged traces
# First let's see what subthreshold responses may look like:
# singleneuron_data.get_ttlonmeasures_fromrawdata()
# singleneuron_data.ttlon_measures.plot.scatter('baselinev', 'response_maxamp')
# there's a clear split: anything with response_maxamp < 20mV are gonna be subthreshold responses; 60 - 80mV will be APs.

subthreshold_responses_df = singleneuron_data.ttlon_measures[(singleneuron_data.ttlon_measures.response_maxamp < 30)]

nodrug_sr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('Stim_00')]
yesdrug_sr_df = subthreshold_responses_df[subthreshold_responses_df.file_origin.str.contains('WithSulpiride_00')]

figure1, axes1 = plot_ttlaligned(singleneuron_data.blocks, nodrug_sr_df,
                                 do_baselining=False,
                                 plotdvdt=False, prettl_t_inms=10, postttl_t_inms=150)
figure1.suptitle('no drug')
axes1[0].set_ylim([-85, -40])

# in the no-drug condition, there are three different light intensity conditions. Splitting those out:
nodrug_light5_sr_df = subthreshold_responses_df[]


figure2, axes2 = plot_ttlaligned(singleneuron_data.blocks, yesdrug_sr_df,
                                 do_baselining=False,
                                 plotdvdt=False, prettl_t_inms=10, postttl_t_inms=150)
figure2.suptitle('with drug')
axes2[0].set_ylim([-85, -40])


