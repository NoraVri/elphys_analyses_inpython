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

neuron_name = '20240703D'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Neat enough seal (~1GOhm) and patch (@t=95.28s in gapFree_0000). Fires off a handful of APs right after break-in,
# then stays subthreshold at Vm~-45--50mV without DC.
# At the end of recordings, cell needs no DC to keep subthreshold at -60mV.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks very sensical. Looks like responses were picked up very neatly, all points have latency 2.5 - 8ms.
# By amplitude, there is a clear separation between subthreshold (<26mV) and AP responses (>65mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
#                             postttl_t_inms=100)
# Indeed, these are all APs, and <40mV are all neat subthreshold responses.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 40)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)
# No outliers really:
# subthreshold responses all have latencies between 3.2 and 6.4ms, and the distribution looks about as close to normal as possible.

# Having plotted various subsets of the data, I am convinced that at this point there is no reason to exclude any.
ttlonmeasures_sthr = ttlonmeasures_sthr.copy()
# This dataset consists of ... recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was 1 or 2ms;
# Drug applied: Sulpiride;
# Light intensity was mostly 5 or 100%, in no-drug condition one block each also at 15, 30 and 50%
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withSul'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashOut'), 'drug_condition'] = 'wash out'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 15, 30, 50, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = ''
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('15p'),'stim_intensity_pct'] = 15
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('30p'),'stim_intensity_pct'] = 30
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('50p'),'stim_intensity_pct'] = 50
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition', hue_order=drug_conditions,
                size='stim_intensity_pct', size_order=intensity_levels,
                style='ttlon_duration_inms',
                )
plt.title('recording conditions overview')
# Note: there doesn't seem to be a significant shift in baselineV following drug application;
# still, no subthreshold responses recorded for higher baselineV levels after drug application, so it does feel like something must've changed

# %% plots: response sensitivity to light intensity & baseline voltage
# Both stim.intensity and duration were varied, in both drug and non-drug conditions.
# Let's split out by drug condition, and then see all the other variables:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           col='ttlon_duration_inms'
           )
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='ttlon_duration_inms',
           col='stim_intensity_pct'
           )
# with drug
ttlonmeasures_sthr_drug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'with drug']
sns.lmplot(data=ttlonmeasures_sthr_drug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           col='ttlon_duration_inms'
           )
ttlonmeasures_sthr_drug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'with drug']
sns.lmplot(data=ttlonmeasures_sthr_drug, x='baselinev', y='response_maxamp',
           hue='ttlon_duration_inms',
           col='stim_intensity_pct'
           )
# Notes regarding the relationship between response amp. and stimulus intensity:
# With or without drug, there is a clear difference between 5 and 100% light intensity;
# however, the intermediate steps at 15, 30, and 50% intensity do not seem statistically different from 100%
# Even so, increasing the stimulus duration from 1 to 2ms always seems to make the response larger, even if just a little bit

# Note regarding the relationship between response amp. and baseline voltage:
# it's clearly there, looks like 2-3mV increase in amplitude for 20-30mV hyperpolarization; trend identical between drug and no-drug conditions.

# %% plots: response sensitivity to drug
# Let's see this separately for 1ms or 2ms stimulus
ttlonmeasures_sthr_stim1ms = ttlonmeasures_sthr[ttlonmeasures_sthr.ttlon_duration_inms == 1]
# for 1ms stim., drug recordings were made only with 100% stim.intensity. Getting only the relevant subset of the DF:
ttlonmeasures_sthr_stim1ms_100pct = ttlonmeasures_sthr_stim1ms[ttlonmeasures_sthr_stim1ms.stim_intensity_pct == 100]
sns.lmplot(data=ttlonmeasures_sthr_stim1ms_100pct, x='baselinev', y='response_maxamp',
           hue='drug_condition', hue_order=drug_conditions,)
sns.lmplot(data=ttlonmeasures_sthr_stim1ms_100pct, x='baselinev', y='response_maxamp_postttl_t_inms',
           hue='drug_condition', hue_order=drug_conditions)
sns.lmplot(data=ttlonmeasures_sthr_stim1ms_100pct, x='baselinev', y='response_maxdvdt',
           hue='drug_condition', hue_order=drug_conditions)
# No good comparisons to be made in these conditions: no-drug recordings were done at different baselineV, seems with-drug needed more hyperpolarization.
# Not sure what's up with response looking to continue increasing with washout.

ttlonmeasures_sthr_stim2ms = ttlonmeasures_sthr[ttlonmeasures_sthr.ttlon_duration_inms == 2]
sns.lmplot(data=ttlonmeasures_sthr_stim2ms, x='baselinev', y='response_maxamp',
           hue='drug_condition', hue_order=drug_conditions,
           col='stim_intensity_pct')
sns.lmplot(data=ttlonmeasures_sthr_stim2ms, x='baselinev', y='response_maxamp_postttl_t_inms',
           hue='drug_condition', hue_order=drug_conditions,
           col='stim_intensity_pct')
sns.lmplot(data=ttlonmeasures_sthr_stim2ms, x='baselinev', y='response_maxdvdt',
           hue='drug_condition', hue_order=drug_conditions,
           col='stim_intensity_pct')
# Looks like there's a small but significant increase in response amp with drug: ~2mV increase from ~15mV without drug (at lowest stim. intensity)
