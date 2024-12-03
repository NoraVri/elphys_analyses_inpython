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

neuron_name = '240626Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
# notes on recording quality:
# Not the greatest recording: cell held with ~-2nA most of the time to keep -70mV
# rec.file#0000 shows steep dropoff of recording conditions after ~150s (as seen from increased holding current and
# test pulse size); cell is then pretty stable for most of recordings, until dropping off further in rec.file#0004,
# ~450s in (drug washout condition).

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# yes, pretty clear from here, too, that recording conditions aren't stable all the time.
# Let's start by whittling down the ttlonmeasures_df to responses recorded under stable conditions:
starting_conditions = ((ttlonmeasures.file_origin == '2024_06_26_0000.abf') & (ttlonmeasures.segment_idx <= 36))
ttlonmeasures = ttlonmeasures[~starting_conditions]
ending_conditions = ((ttlonmeasures.file_origin == '2024_06_26_0004.abf') & (ttlonmeasures.segment_idx >= 87))
ttlonmeasures = ttlonmeasures[~ending_conditions]
# check and see recording conditions again:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# this looks good, whatever drift there is in recording conditions looks insignificant.

# Now let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# That's looking pretty good. All responses are subthreshold (max.amp <300pA) and no response peak times were measured
# < 1.5ms or >20ms post ttl onset.
# The histogram of response peak times looks somewhat interesting, with two distinct peaks at ~1.8 and ~2.2ms.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# In the response peak times there's two outliers: responses generally peak <3ms post stim., but there are two
# measured much later than that. Let's see:
neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 5],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            )
# Well. Yes in each case it's the second peak of a two-peaked response that got measured, but it really just looks like
# these are the only two two-peaked responses in this dataset.

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 350 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 0.5ms;
# Drug applied: Sulpride;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0626.rtf)
drug_conditions = ['no drug', 'wash in', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0001'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0002'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0004'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# my eye says: statistically no difference between no-drug and drug conditions. Mean looks to be up a tiny bit but
# whiskers in no-drug condition fall entirely within drug-condition ones

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# no difference here either.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
