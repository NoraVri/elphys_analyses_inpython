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

neuron_name = '240724X'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks like a nice enough recording: holding with ~-150pA to keep -70mV and quite stable throughout;
# optoStim responses always subthreshold

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=15)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# Yea that looks quite OK; seems baselinec drifted down a bit from ~-150pA to ~-200pA towards the middle of recordings,
# and then went back up again to the original holding level

# Now let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Looks like all responses are subthreshold by amplitude (<200pA); distribution of peak-times looks a little messy but not impossible.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# distribution of peak-times looks not so neat; earliest ones are 1.3ms post ttl onset, and the distribution seems to
# have multiple peaks (at ~2.5, 3.5 and 5ms) and a funny-looking tail.

neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 6],
                            postttl_t_inms=15,
                            prettl_t_inms=2,
                            )
# Looks like responses are all rather similar - perhaps there's a more steeply rising earlier component and a
# more rounded, later component; but it also looks like gain settings not optimal for seeing such minute things

# Having looked at all the recorded responses, I am convinced that the response peaks were all measured appropriately given the raw data.

# This dataset consists of 500 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was 1ms
# Drug applied: CGP55845;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0724.rtf, cell 2)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0006'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0007'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0008'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0009'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
plt.figure()
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')


for drug_condition in drug_conditions:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == drug_condition],
                                postttl_t_inms=15,
                                prettl_t_inms=2,
                                newplot_per_ttlduration=True,
                                plt_title=drug_condition)

# Doesn't look like anything changed significantly with drug application, except maybe baselinec

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
