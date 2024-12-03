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

neuron_name = '240530Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks decent enough: ~-200pA to keep -70mV; stability not great though, holding current decreasing steadily
# and capacitance artefacts increasing suddenly just before drug application

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# Indeed, holding current ~-100pA during first recording block, then suddenly down to ~-170 for the rest of recordings.
# Not sure we can call this a drug effect, as DeNard told me he starts wash-in with new recording file
# (i.e. we should see the effect come on during the first block with drug, not before).

# Let's see some more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# interesting: responses generally peak ~5ms post ttl onset, but after drug application a decent proportion of
# responses peak by ~2ms post ttl. From looking at the raw data, it seems responses generally have multiple peaks,
# usually summing such that the last one marks the maximal amplitude of the response

# Besides the issues mentioned above, data is looking pretty good: responses are all subthreshold (<250pA) and
# occurring 1.5 - 7ms post ttl (one outlier at 9ms post ttl).

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# Not sure if there's really any outliers, or just variance in the raw data.

neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 3],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            )
# The responses all look real; the small handful of responses that's smaller than the rest (~75pA vs ~175pA on avg.)
# are the only responses with just a single peak. And while it definitely seems like drug had something to do with
# response peaks getting measured earlier, these responses are very much interspersed with the ones peaking at ~5ms
# so no reason to assume that this happened because of some other change in recording conditions.
# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 500 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 0.25ms;
# Drug applied: Sulpride;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0530.rtf, cell 2)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0006'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0007'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0008'), 'drug_condition'] = 'wash out'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0009'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# Looks like there might be an effect there, but it's nothing impressive: going from ~150pA to ~175pA on avg.,
# with amplitude variance being ~75pA regardless of drug condition

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# nothing much to be seen here, either; clear from here that early-peaking responses appear only once drug is applied

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')