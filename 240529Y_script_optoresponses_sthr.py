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

neuron_name = '240529Y'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Seems like a pretty neat recording: baselinec going from ~0 to -100pA during the first recording block, then
# going down further with drug application; capacitance a little wobbly especially at first, but mostly pretty stable.
# Clearly visible spont.depolarizing events, especially during the last recording block.

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=50)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# Definitely a lot less current is used during the first block to keep -70mV (~-50pA vs ~-150pA later on), but
# with baselinec coming back up again during the final recording block this may be a drug effect

# Let's see some more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# This all looks nice: response peak times are between 3 and 6 ms post ttl,
# and it looks like all responses are subthreshold (~50-550pA amplitude).

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# Looks like there aren't really outliers in this data.

for file in ttlonmeasures_sthr.file_origin.unique():
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.file_origin == file],
                            postttl_t_inms=25,
                            prettl_t_inms=5,
                            )
# These all look like neat, simple synaptic responses.
# However, the first recording block has me suspicious: there appears to be a relationship between baselinec
# getting increasingly more negative (going from ~-30 down to -100pA) and response amp. getting smaller
# (>500pA at first, ~300pA with baselinec -100pA).
# In the last two recording block, there is one recording trace where response fails/is very small compared to all others.

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately
# given what's in the raw data.

# This dataset consists of 500 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 0.5ms;
# Drug applied: Sulpride; then washed with Quinpirole - ?
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0529.rtf, cell 1)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0001'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0002'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0003'), 'drug_condition'] = 'wash out'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0004'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
#Interesting. Baselinec seems to behave as expected: steadily dropping during the first recording block then
# steeply dropping before stabilizing with drug application, to come back up again with drug washout.
# However, the response amplitudes don't follow this trend: they just get increasingly smaller over the course of recordings.
sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# Mean peak times don't change, variance seems to increase significantly over the course of recordings.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

