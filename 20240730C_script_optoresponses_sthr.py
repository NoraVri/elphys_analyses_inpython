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

neuron_name = '20240730C'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Neat sealing (just under 2GOhm) and break-in, cell spiking with freq.~40Hz, quiet when held at ~-55mV w/-150pA DC
# baselineV seems to go down after application of quinpirole, but AP parameters look practically unchanged throughout recordings

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=40)  # adjusted from default - see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks mostly sensical.
# By amplitude, there is a clear separation between subthreshold (<6mV) and AP responses (>30mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 20],  # [ttlonmeasures.response_maxamp < -1]
#                             postttl_t_inms=100)
#                             indeed, these are all APs, mostly in traces where spont.spiking is on (all except 2 traces).
# A couple of them have bad baselinev because of that - not gonna deal with that here though, since we are interested in subthreshold responses only at the moment.
# One response peak was measured at the very end of the chosen 40ms response window, and one at the start.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[((ttlonmeasures.response_maxamp < 20) & (ttlonmeasures.response_maxamp > 0))]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# No subthreshold responses got measured close to the stimulus, they all occur >3.5ms post
# On the side of too long after the stimulus:
# There's 7 subthreshold responses that got measured as peaking >20ms; there is always a peak, and it's always <40ms from the stimulus.
## Re-running get_ttlonmeasures_fromrawdata with 40ms response window
# There's just one response that got measured at the end of the 40ms window - it's in a trace where the neuron is spiking spontaneously, that's why voltage doesn't decay back down.

neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 35],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            )
# Having plotted various subsets of the data, I am convinced that only the one response was mismeasured and needs to be excluded.
# Whittling down the DF accordingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 39]
# This dataset consists of 465 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was 1 or 5ms;
# Drug applied: Quinpirole;
# Light intensity was 100% for all recordings except one block recorded with 5%
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = ''
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition',
                size='stim_intensity_pct',
                style='ttlon_duration_inms')
# Note: slight shift in baselineV following drug application (Vm down by ~2mV for the same DC)

# %% plots: response sensitivity to light intensity & baseline voltage
# In the no drug condition, there is one block where stim.intensity was 5% (duration 1ms),
# and one block where stim.duration was 5ms (intensity 100%); all others were recorded with stim.intensity 100% for 1 ms.

# Filtering down the DF for proper comparisons:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']

ttlonmeasures_sthr_nodrug_stim1ms = ttlonmeasures_sthr_nodrug[ttlonmeasures_sthr_nodrug.ttlon_duration_inms == 1]
sns.lmplot(data=ttlonmeasures_sthr_nodrug_stim1ms, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
# That's pretty clear: going from 5 to 100% stim.intensity increased response amplitude from ~1.5 to ~4.5mV

ttlonmeasures_sthr_nodrug_stim100pct = ttlonmeasures_sthr_nodrug[ttlonmeasures_sthr_nodrug.stim_intensity_pct == 100]
sns.lmplot(data=ttlonmeasures_sthr_nodrug_stim100pct, x='baselinev', y='response_maxamp',
           hue='ttlon_duration_inms',
           )
# That's pretty clear, too: no real change in response for increasing stim.duration from 1 to 5ms

# Note on relationship between baselineV and response amp: there is a large spread of response amplitudes (~2-9mV)
# at each recorded level of baselineV (-80 - -60mV), with no clear trend (if anything, larger responses are more likely to occur at more depolarized baselineV).

# %% plots: response sensitivity to drug
# drug recordings were all done with 1ms light stim duration at 100% intensity. Getting the relevant subset of the DF:
ttlonmeasures_sthr_stim100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]
ttlonmeasures_sthr_stim100pct_1ms = ttlonmeasures_sthr_stim100pct[ttlonmeasures_sthr_stim100pct.ttlon_duration_inms == 1]

sns.lmplot(data=ttlonmeasures_sthr_stim100pct_1ms, x='baselinev', y='response_maxamp', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stim100pct_1ms, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stim100pct_1ms, x='baselinev', y='response_maxdvdt', hue='drug_condition')
# What this looks like is that applying the drug has no effect on the response to optoStim.
# If there is any effect at all, it's on the decays of the responses: they look more neat and tight when drug is applied
neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim100pct_1ms[ttlonmeasures_sthr_stim100pct_1ms.drug_condition == 'no drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            )
neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim100pct_1ms[ttlonmeasures_sthr_stim100pct_1ms.drug_condition == 'with drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            )
