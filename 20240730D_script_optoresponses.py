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
# neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
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
# their peak at the edge of the response window should be excluded.
# Whittling down the DF accodingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 7.8]
# This dataset consists of 753 recorded subthreshold responses.
# %%



























# %% getting optoStim response measurements:
# neuron_data.get_ttlonmeasures_fromrawdata()
# ttlonmeasures = neuron_data.ttlon_measures.copy()
#
# # check and see response_maxamp_postttl_t_inms - does it make sense?
# ttlonmeasures.plot.scatter('response_maxamp', 'response_maxamp_postttl_t_inms')
# ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=100)
#
# # let's see some of the outliers:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms < 2])
# # just one response here: it's riding the decay of a depolarization occurring spontaneously ~10ms before the light comes on
# # unusual measurement because of unusual experimental condition arising spontaneously: datapoint can be excluded
#
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms > 6]) # tried 6, 7, 8, 9ms
# # these responses look OK, but with additional depolarizing events in the trace soon after optoStim response

# Forcing algorithm to search for peaks in smaller window should ease this. Let's do so:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=10)
ttlonmeasures = neuron_data.ttlon_measures.copy()
# check and see response_maxamp_postttl_t_inms again
ttlonmeasures.plot.scatter('response_maxamp', 'response_maxamp_postttl_t_inms')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=100)

neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms > 6])
neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms > 9.9])
# the three responses with 'peaks' measured at the 10ms search window edge are mismeasurements
# (rising phase not over yet), but otherwise all these traces look proper.

ttlonmeasures = ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms < 9.9]
neuron_data.ttlon_measures = ttlonmeasures.copy()
neuron_data.write_results()


# # %% notes on optoStim experiments:
# ttlonmeasures = neuron_data.ttlon_measures.copy()
# # ttlonmeasures.file_origin.unique()
# # ttlonmeasures.ttlon_duration_inms.unique()
# # ttlonmeasures.plot.scatter(x='applied_current', y='baselinev')
#
# # Light stim duration was varied (1, 2, 5 ms)
# # Light intensity was not varied; 100% all around
# # Various levels of holding current applied to change baselineV.
# # Looks like recording conditions drifted: there are wide ranges of baselineV values at each holding level, sometimes even multiple clusters.
#
# # Adding drug conditions as a column to ttlonmeasures dataframe:
# drug_conditions = ['no drug', 'wash in', 'with drug']
# # ttlonmeasures.loc[:, 'drug_condition'] = 'no drug'
# # ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
# # ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'
#
# # Adding light intensity as a column to ttlonmeasures dataframe:
# intensity_levels = [100]
# # ttlonmeasures.loc[:,'stim_intensity_pct'] = ''
# # ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100
#
# # Adding holding current as a categories-column to ttlonmeasures dataframe:
# # Since there are a lot of levels, I won't enter the groups manually; using quicker grouping instead:
# holding_currents_series = ttlonmeasures.applied_current
# holding_currents_rounded_series = (holding_currents_series / 10).round(decimals=0) * 10
# # ttlonmeasures.loc[:, 'applied_current group'] = holding_currents_rounded_series
# holding_current_levels = holding_currents_rounded_series.unique().tolist()
# holding_current_levels.sort()
#
# # Adding baselinev as a categorical variable to ttlonmeasures dataframe by rounding to no decimals:
# # baselinev = ttlonmeasures.baselinev
# # binned_baselinev = baselinev.round(decimals=0)
# # ttlonmeasures.loc[:, 'binned_baselinev'] = binned_baselinev
#
# # neuron_data.ttlon_measures = ttlonmeasures.copy()
# # neuron_data.write_results()
#
# # Seeing whether drug and no-drug conditions are comparable in terms of holding current/baselineV relationship:
# plt.figure()
# sns.boxplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
# plt.figure()
# sns.stripplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
# # conclusion: Looks like baselineV comes way down with quinpirole application, by about 20mV.
#
# # %% filtering responses - check for APs and post-ttl peak time
# # check and see: are APs and subthreshold responses easy to distinguish?
# # ttlonmeasures.plot.scatter('baselinev', 'response_maxamp')
# # indeed they are: APs are 30mV or larger in amplitude, while the subthreshold response mostly is 3mV or smaller.
# ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 20]
#
# # check and see: do peak times post-ttl make sense?
# ttlonmeasures.plot.scatter('response_maxamp', 'response_maxamp_postttl_t_inms')
# ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=100)
# # looks like response peaks generally occur 2 - 7ms post ttl; let's see the responses that fall outside that window:
#
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms < 2])
# # just one response here: it's riding the decay of a depolarization occurring spontaneously ~10ms before the light comes on.
#
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms > 6])
#
# # %% opto response sensitivity to light intensity & baseline voltage
# # getting ttlonmeasures_df for non-drug runs only:
# ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[(ttlonmeasures_sthr.drug_condition == 'no drug')]
#
# # light intensity is always 100%, we do have different stimulation durations (1, 2 and 5ms).
# # Let's see if changing duration does anything:
# plt.figure()
# sns.stripplot(data=ttlonmeasures_sthr_nodrug, x='applied_current group', y='response_maxamp', hue='ttlon_duration_inms', order=holding_current_levels, hue_order=[1, 2, 5])
# sns.boxplot(data=ttlonmeasures_sthr_nodrug, x='applied_current group', y='response_maxamp', hue='ttlon_duration_inms', order=holding_current_levels, hue_order=[1, 2, 5], fill=False)
# # Different durations were applied only for holding level -750pA; response amplitudes look statistically practically identical for each duration.
# # Still, let's take only 1ms light duration trials for consistency:
# ttlonmeasures_sthr_nodrug_1ms = ttlonmeasures_sthr_nodrug[ttlonmeasures_sthr_nodrug.ttlon_duration_inms == 1]
#
# plt.figure()
# sns.lineplot(data=ttlonmeasures_sthr_nodrug_1ms, x='binned_baselinev', y='response_maxamp',
#              # hue='applied_current group'
#              )

