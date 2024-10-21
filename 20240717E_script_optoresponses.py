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

neuron_name = '20240717E'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice seal (just under 2MOhm) and patch (@t=55.12 in gapFree_0000). While cell-attached, AP freq looks to be ~30Hz;
# on break-in, AP freq is ~60Hz.
# Cell seems somewhat unsteady about baselineV and AP parameters, may not be the greatest recording

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this all looks perfectly sensical. Looks like responses were picked up very neatly; max. latency is ~13ms.
# By amplitude, there is a clear separation between subthreshold (<28mV) and AP responses (>60mV). Check to see:
# # neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
# #                             postttl_t_inms=100)

# Indeed, these are all APs.
# Next looking at all subthreshold responses, at first glance they all look great; seems this neuron wasn't doing much else besides responding to light, i.e., no spontaneously occurring depolarizations to muck things up.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 40)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# No responses got measured too soon after stim., the shortest latency is ~3.5ms.
# On the side of too long after the stimulus:
# No responses got measured too long after stim., the longest latency is 12.2ms.

ttlonmeasures_sthr = ttlonmeasures_sthr.copy()
# This dataset consists of 426 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Quinpirole;
# Light intensity was 5% most of the time, 50 and 100% applied only during drug washout
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashOut'), 'drug_condition'] = 'wash out'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 50, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = ''
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('50p'),'stim_intensity_pct'] = 50
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition', hue_order=drug_conditions,
                size='stim_intensity_pct',
                )
plt.title('recording conditions overview')
# Note: looks like there is a slight shift in baselineV in response to the drug,
# but it's also highly plausible that the data is just messy

# %% plots: response sensitivity to light intensity & baseline voltage
# All blocks were recorded with light duration 1ms; intensity was varied in washout condition only.
# Getting the relevant subset of the DF:
ttlonmeasures_sthr_washout = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'wash out']
sns.lmplot(data=ttlonmeasures_sthr_washout, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
plt.title('drug washout')
# Response amplitudes are all between 10 and 28mV; otherwise, this is a random-looking cloud of dots.
# Changing light intensity does not seem to have a systematic effect on response amplitude.
# Changing baseline voltage does not seem to have a systematic effect on response amplitude.

# %% plots: response sensitivity to drug
# drug recordings were all done with 1ms light stim duration at 5% intensity. Getting the relevant subset of the DF:
ttlonmeasures_sthr_stim5pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 5]

sns.lmplot(data=ttlonmeasures_sthr_stim5pct, x='baselinev', y='response_maxamp',
           hue='drug_condition', hue_order=drug_conditions)
sns.lmplot(data=ttlonmeasures_sthr_stim5pct, x='baselinev', y='response_maxamp_postttl_t_inms',
           hue='drug_condition', hue_order=drug_conditions)
sns.lmplot(data=ttlonmeasures_sthr_stim5pct, x='baselinev', y='response_maxdvdt',
           hue='drug_condition', hue_order=drug_conditions)

neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim5pct[ttlonmeasures_sthr_stim5pct.drug_condition == 'no drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='no drug'
                            )
neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim5pct[ttlonmeasures_sthr_stim5pct.drug_condition == 'with drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='with drug'
                            )
# If there is any difference at all between these two conditions, it's that with drug, there aren't any
# subthreshold responses recorded at Vm ~-70mV (the most depolarized potential).
# Possibly, they're APs instead; would have to look into that.
