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
# neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')

# Very nice sealing and break-in (@t=77.373s in gapFree_0000) while neuron spiking with freq just below 40Hz.
# AP peakV ~+20mV, AHPmin ~-47mV initially, keeps at ~-70mV w/ -100pA DC;
# After optoStim experiments, holding increased a bit to -150pA to keep ~-70mV and AP parameters look practically unchanged.
# Active properties look to have deteriorated after longPulse experiments, which were performed at the end of recordings.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=150)
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
# having plotted various responses this way, I am convinced that responses with peaktime >40ms post ttl should be
# excluded from analyses. Of these 12 traces, one is a complex response containing many depolarizations;
# the others are traces where a small light response is followed by a large spontaneous depolarization ~100ms later.
# Responses with baselinev_range > 0.5mV should also be excluded; in these traces, a spontaneous depolarization is already underway when the light is applied.
# Whittling down the subthreshold responses DF accordingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms < 40]
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.baselinev_range <= 0.5]
# This dataset consists of 442 recorded subthreshold responses. (11 small responses were excluded )
# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
ttlonmeasures_sthr.file_origin.unique()
ttlonmeasures_sthr.ttlon_duration_inms.unique()
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
