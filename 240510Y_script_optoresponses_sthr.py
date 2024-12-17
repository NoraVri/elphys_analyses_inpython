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

neuron_name = '240510Y'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Just three recording blocks; neuron dies quickly and suddenly during the last one.
# Otherwise looking like a pretty neat recording: cell held with ~-150pA to keep -60mV;
# capacitance looking relatively steady; and not much in the way of spontaneously generated activity.

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=50)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# very obvious sudden drop in baselinec indicating where neuron dies. Excluding sweeps where neuron is dead:
ttlonmeasures = ttlonmeasures[ttlonmeasures.baselinec > -1000]


# Now let's see response parameters:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# This mostly looks neat: responses are all subthreshold (~75 - 350pA) and
# peak times between ~1.5 and 5 ms (plus a few more up to 7ms post ttl).
# Notably though, peak times do not look normally distributed, with a kind of fuzzy boundary visible ~3ms

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
# Looks like this distinguishes between responses that have a single steep rise and then decay, vs responses that
# have more of a compound rise and/or plateau before decaying again.
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200, by='file_origin', sharex=True, sharey=True)
# Seems like both types of responses are present in all recording files,
# making it unlikely to be an effect of recording conditions changing in some way.

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately
# given what's in the raw data.

# This dataset consists of 259 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 0.25ms;
# Drug applied: Quinpirole;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0529.rtf, cell 1)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0007'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0008'), 'drug_condition'] = 'with drug'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# Hmm. Response amplitude drops significantly with drug wash in, then goes back up with drug fully applied.
# Baselinec also drops with wash in, then goes back up to pre-drug level.

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# Interesting: seems once drug is fully applied, late-peaking responses are in the majority (50/50 before then).

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')



