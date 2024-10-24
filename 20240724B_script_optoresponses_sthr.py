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

neuron_name = '20240724B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Not exactly perfect seal (just under GOhm) and -100pA DC applied on break-in (@t=336.39s in gapFree_0000).
# Looks like all cell-health parameters may be drifting a bit over the course of recordings, although neuron is mostly
# hanging on nicely throughout the half hour of recordings

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks very sensical. Looks like responses were mostly quite neat: most have latency <15ms, three responses have latency of ~21ms.
# By amplitude, there is a clear separation between subthreshold (<18mV) and AP responses (>60mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 60],
#                             postttl_t_inms=100)
# Indeed, these are all APs.
# Next looking at all subthreshold responses, it seems to me that all peaks were picked up perfectly.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 60)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)
# First, on the side of too soon after the stimulus:
# No responses got measured too soon after stim.on, latencies are >3.3ms for all responses.
# On the side of too long after the stimulus:
# No responses were measured anywhere close to the end of the 150ms response window; only two with latency >20ms, and these look properly picked up.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 20],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )

# Having plotted various subsets of the data, I am convinced that these are all proper subthreshold responses.
ttlonmeasures_sthr = ttlonmeasures_sthr.copy()
# This dataset consists of 322 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Quinpirole;
# Light intensity was 5, 50 or 100% (varied only in non-drug condition)
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
                size='stim_intensity_pct',
                )
plt.title('recording conditions overview')

# %% plots: response sensitivity to light intensity & baseline voltage
# All blocks were recorded with light duration 1ms; intensity was varied in the non-drug condition only.
# Getting the relevant subset of the DF:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
plt.title('no drug applied')
# That looks like there is some sensitivity to light intensity: responses are generally smallest at intensity=5%, by ~3mV.
# However, at 50 and 100% intensity response amplitudes are practically identical (generally lots of jitter in
# response amps, ranges between 7-14mV for stim.50 or 100%).

# Note on the relationship between baselineV and response amp.: no clear effect of hyperpolarization increasing
# response amp, lines look practically flat; if there is any effect at all, it's that larger amp responses are
# more likely to occur at more depolarized Vm.

# %% plots: response sensitivity to drug
# recordings with drug were all performed at 100% light intensity. Getting the relevant subset of the DF:
ttlonmeasures_sthr_stim100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxdvdt', hue='drug_condition')
# Doesn't look like drug has effect on response amplitude at all, let alone a significant one.
# Interestingly though, the distribution of post-ttl-peak times does look different between drug/no drug conditions.
# Hard to say if that's really a drug effect though or just an effect of the cell getting tired.
neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim100pct[ttlonmeasures_sthr_stim100pct.drug_condition == 'no drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='no drug'
                            )
neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stim100pct[ttlonmeasures_sthr_stim100pct.drug_condition == 'with drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='with drug'
                            )

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')


