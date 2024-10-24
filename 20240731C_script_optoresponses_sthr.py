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

neuron_name = '20240731C'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')

# Very nice sealing and break-in (@t=77.373s in gapFree_0000) while neuron spiking with freq just below 40Hz.
# AP peakV ~+20mV, AHPmin ~-47mV initially at freq.~40Hz w/oDC, keeps at ~-70mV w/ -100pA DC;
# After optoStim experiments, holding increased a bit to -150pA to keep ~-70mV and AP parameters look practically unchanged.
# Active properties look to have deteriorated after longPulse experiments, which were performed at the end of recordings.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=40)  # re-set from default, see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks mostly sensical.
# By amplitude, there is a clear separation between subthreshold (<13mV) and AP responses (>40mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
#                             postttl_t_inms=100)
#                             indeed, these are all APs.
# No response peaks were measured at the very end of the chosen 150ms response window.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 40]

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# the scatter plot is quite clear: the earliest peaks of subthreshold responses occur no less than 4.5ms post-stimulus,
# meaning they are in good range to be monosynaptic responses to the stimulus.
# On the side of too long after the stimulus:
# the histogram shows one main peak at ~8ms post stimulus, another much smaller peak ~15ms and then a very long tail
# that has a big gap in it between 35 and 59ms post stimulus.

# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 40],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.baselinev_range > 0.5],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# having plotted various responses this way, I am convinced that responses with peaktime >40ms post ttl do not properly
# reflect the peak of the light response. Of these 12 traces, one is a complex response containing many depolarizations;
# the others are traces where a small light response is followed by a large spontaneous depolarization ~100ms later.
# Responses with baselinev_range > 0.5mV should also be excluded; in these traces, a spontaneous depolarization is already underway when the light is applied.
## Re-running get_ttlonmeasures_fromrawdata with 40ms window
# After re-running with 40ms window, there are 4 responses that get measured at the very end. Seeing them, these are
# measured on the rising slope of APs (two in a spont.spiking record, two on slow-rising AP responses). Just below that
# with latency ~35ms is the one 'complex response' we saw before, it's first but smallest peak got picked up here.
# Since as a single response among hundreds it's an outlier, I feel comfortable excluding it from this data.
# Whittling down the subthreshold responses DF accordingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms < 35]
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.baselinev_range <= 0.5]
# This dataset consists of 455 recorded subthreshold responses.
# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Quinpirole;
# Light intensity was varied (5, 50 and 100%) in no-drug condition only;
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 50, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = ''
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('50p'),'stim_intensity_pct'] = 50
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition',
                size='stim_intensity_pct')


# %% plots: response sensitivity to light intensity & baseline voltage
# light intensity was varied in no-drug condition only. Getting the relevant subset of the dataframe:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']

sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp', hue='stim_intensity_pct')
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp_postttl_t_inms', hue='stim_intensity_pct')
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxdvdt', hue='stim_intensity_pct')
# Response parameters all look to be systematically sensitive to light intensity;
# much larger change going from 5 to 50%, than from 50 to 100%.

# %% plots: response sensitivity to drug
# drug recordings were done with 100% light intensity only. Getting the relevant subset of the dataframe:
ttlonmeasures_sthr_maxintensity = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]

sns.lmplot(data=ttlonmeasures_sthr_maxintensity, x='baselinev', y='response_maxamp', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_maxintensity, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_maxintensity, x='baselinev', y='response_maxdvdt', hue='drug_condition')

# Looks like the response amplitude increases from ~6 to ~8mV with drug.
# Note: response amp is highly variable across the board, but especially at the most depolarized Vm ~-65mV: 3 - 12mV amps

# Note on relationship between baselineV and response amplitude: doesn't look like there is one,
# response amp way too variable at each baselineV level for a trend to be visible

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

