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

neuron_name = '240521Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks like a pretty nice recording. Cell held with ~-150pA (and dropping a bit) to keep -70mV; capacitance artefact
# not entirely steady, but no spikes and very little in the way of spontaneously occurring depolarizations.

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=50)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# baselinec dropping steadily during the first two recording blocks; likely to be drug effect

# Let's see some more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# This mostly looks neat: responses are all subthreshold (~50 - 160pA) and peak between 2 and 8ms post ttl.
# Interestingly though, peak times appear to come in two groups, with a sharp divide at ~3ms.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# Looks like there aren't really outliers in this data; just that grouping in response peak times.

neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms < 3],  #> 3
                            postttl_t_inms=25,
                            prettl_t_inms=5,
                            )
# Interesting. It's all rather noisy, but it seems like the later-peaking responses (which are the majority)
# consist of two parts summing together, whereas the early-peaking responses have only a single depolarizing phase.

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately
# given what's in the raw data.

# This dataset consists of 400 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 1ms;
# Drug applied: Quinpirole; then washed with Sulpride - ???
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0529.rtf, cell 1)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0001'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0002'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0003'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# response amplitude looks like it drops a little on average; whiskers fully overlapping though.
# Also, drop continues with drug washout.

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# Looks like no difference between conditions.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
