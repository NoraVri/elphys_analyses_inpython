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

neuron_name = '20240724C'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice seal (~3GOhm) and patch (@t=84.23s in gapFree_0000). Cell spiking with freq ~40Hz as seen cell-attached, >35Hz on break-in,
# then held subthreshold ~-65mV with -125pA DC. After drug application, cell needs -150pA to stay subthreshold ~-70mV,
# and spontaneous firing freq. seems to have gone up to >50Hz.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks mostly sensical. Looks like responses were mostly quite neat, all but two got picked up with peak posttl_t < 20ms, longest latency is just over 60ms.
# By amplitude, there is a clear separation between subthreshold (<30mV) and AP responses (>60mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
#                             postttl_t_inms=100)
#                             indeed, these are all APs. Notably, neuron not spiking spontaneously in a lot of these traces; it looks like for baselineV ~-75mV, APs can still be evoked (with delays up to 30ms post stim.)

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 40)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# No responses got measured too soon after stim.on, latencies are >3.5ms for all responses.
# On the side of too long after the stimulus:
# No responses were measured anywhere close to the end of the 150ms response window; only two with latency >20ms, and these look properly picked up (these two are also occurring at the most depolarized Vrest while still being subthreshold).
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 20],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )

# Having plotted various subsets of the data, I am convinced that these are all proper subthreshold responses.
ttlonmeasures_sthr = ttlonmeasures_sthr.copy()
# This dataset consists of 336 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Quinpirole;
# Light intensity was 5, 50 or 100% (varied also during drug application)
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
# Note: looks like there is a significant shift in baselineV following drug application, Vm up by ~10mV for the same DC holding level

# %% plots: response sensitivity to light intensity & baseline voltage
# All blocks were recorded with light duration 1ms; intensity was varied, both in drug and non-drug conditions.
# Making a separate plot for drug and non-drug conditions:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
plt.title('no drug applied')

ttlonmeasures_sthr_drug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'with drug']
sns.lmplot(data=ttlonmeasures_sthr_drug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
plt.title('drug applied')

# In both conditions, there is sensitivity to light intensity: the lowest light intensity gives the smallest responses.
# In the drug condition, it looks like the difference between 50 and 100% light intensity may not be significant;
# definitely it's messy, with responses for 50% intensity often being larger than for 100% intensity.

# Note on the relationship between baselineV and response amp.: no clear effect of hyperpolarization increasing response amp, lines look mostly flat.

# Note on drug effect: from these plots, it looks like response amplitudes increased the most for the 5% stimulus
# (2-fold increase from ~6 to ~12mV amp), and the least for the 100% stimulus (~3mV increase from 14mV).

# %% plots: response sensitivity to drug
# drug recordings were done at each of the three intensity levels. Splitting out the DF accordingly:
ttlonmeasures_sthr_stim5pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 5]
sns.lmplot(data=ttlonmeasures_sthr_stim5pct, x='baselinev', y='response_maxamp', hue='drug_condition')
plt.title('stim intensity 5%')
# sns.lmplot(data=ttlonmeasures_sthr_stim5pct, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# sns.lmplot(data=ttlonmeasures_sthr_stim5pct, x='baselinev', y='response_maxdvdt', hue='drug_condition')


ttlonmeasures_sthr_stim50pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 50]
sns.lmplot(data=ttlonmeasures_sthr_stim50pct, x='baselinev', y='response_maxamp', hue='drug_condition')
plt.title('stim intensity 50%')
# sns.lmplot(data=ttlonmeasures_sthr_stim50pct, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# sns.lmplot(data=ttlonmeasures_sthr_stim50pct, x='baselinev', y='response_maxdvdt', hue='drug_condition')


ttlonmeasures_sthr_stim100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp', hue='drug_condition')
plt.title('stim intensity 100%')
# sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxdvdt', hue='drug_condition')

# As noted before, the drug effect seems largest when stim.intensity is lowest.
# Other than that, this data all looks perfectly sensical.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

