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

neuron_name = '20240730D'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Pretty strange recording: neat sealing (~4GOhm) and break-in, yet AP peakVs highly variable from the start
# AP freq is high yet irregular (that is: intervals between spont.APs usually very short, but behavior kinda bursty overall).
# Needs - 300pA to keep from spontaneously spiking at ~-50mV to start with; by the end of recordings -250pA keeps -60mV.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=8)  # adjusted from default - see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks mostly sensical.
# By amplitude, there is a clear separation between subthreshold (<6mV) and AP responses (>30mV),
# and one 'response' has amplitude -20mV - that's gonna be an AP. Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 20],  # [ttlonmeasures.response_maxamp < -1]
#                             postttl_t_inms=100)
#                             indeed, these are all APs.
# They occur mostly in traces where neuron is spontaneously spiking (except lowest baselinev level).
# A couple of them have bad baselinev because of that - not gonna deal with that here though, since we are interested in subthreshold responses only at the moment.
# No response peaks were measured at the very end of the chosen 40ms response window, and just one at the start.
# With the 8ms response window, there are 3 that are measured at the end of the window.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[((ttlonmeasures.response_maxamp < 20) & (ttlonmeasures.response_maxamp > 0))]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# There's one response that's measured <1ms post ttl, and it's in a trace where spontaneous depolarizations are occurring already before the stimulus.
# it actually has a small negative amplitude and got filtered out when we filtered for subthreshold responses.
# On the side of too long after the stimulus:
# It looks to me that any response measured more than 40ms post ttl onset (45 traces) are really spontaneous
# depolarizations that are larger than the stimulus-evoked response (which is also there in each of these traces).
## Re-running get_ttlonmeasures_fromrawdata with 40ms response window
# I'm seeing the same problem still: there is always a response and it's always within 8ms from the stimulus.
# It's just very small sometimes, and depolarizations happening spontaneously and frequently are larger
## Re-running get_ttlonmeasures_fromrawdata with 8ms response window
# The three responses measured at 8ms post ttl are indeed mismeasurements: two APs, and one more prolonged (~10ms) depolarization.

# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms < 1],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 7.8],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# Having plotted various subsets of the data, I am convinced that the three 'responses' measured as having
# their peak at the edge of the response window should be excluded; all other responses look proper.
# Whittling down the DF accodingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 7.8]
# This dataset consists of 753 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was 1, 2 or 5ms;
# Drug applied: Quinpirole;
# Light intensity was 100% for all recordings
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition',
                style='ttlon_duration_inms',
                )
# Note: significant shift in baseline voltage following drug application (Vm way down, requiring ~400pA less DC to keep same level as before drug).

# %% plots: response sensitivity to light intensity & baseline voltage
# light intensity was not varied, but stimulus duration was, in no-drug condition only.
# Getting the relevant subset of the dataframe:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']

sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='ttlon_duration_inms',
           )
# Looks like increasing stimulus duration had no effect on the response.
# Note on relationship between response amp and baselineV: it seems like larger (3-4mV) responses are slightly more
# likely to occur at more depolarized Vm; then again there does not appear to be any systematic relationship between
# Vm and response amplitude (~1.5mV on avg. for -90 < Vm < -50).

# %% plots: response sensitivity to drug
# drug recordings were all done with 1ms light stim duration only. Getting the relevant subset of the dataframe:
ttlonmeasures_sthr_stim1ms = ttlonmeasures_sthr[ttlonmeasures_sthr.ttlon_duration_inms == 1]

sns.lmplot(data=ttlonmeasures_sthr_stim1ms, x='baselinev', y='response_maxamp', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stim1ms, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stim1ms, x='baselinev', y='response_maxdvdt', hue='drug_condition')
# Looks like there is a significant increase in response amplitude with drug, from 1.5 w/o to 2.5mV w/ drug.
# In line with this, there is a slight increase in maxdVdt of the responses with drug.

neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim1ms[ttlonmeasures_sthr_stim1ms.drug_condition == 'no drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='no drug'
                            )
neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim1ms[ttlonmeasures_sthr_stim1ms.drug_condition == 'with drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='with drug'
                            )

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
