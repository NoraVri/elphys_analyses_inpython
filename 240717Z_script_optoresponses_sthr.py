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

neuron_name = '240717Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
# notes on recording quality:
# Seems like a real nice recording, cell held with just ~-50pA to keep -60mV and looking very stable throughout
# (except for a few sweeps in longPulses where it's a lot more leaky all of a sudden, but that's at the end of recordings and then it recovers)
# I do see cell responding to stim. with AP regularly, more so towards the end of recordings.

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=15)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# Looks very neat: holding current getting a little less negative over the course of recordings, going from ~-90 to ~-50pA; probably has more to do with drug application than any other change in recording conditions.

# Now let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Clear grouping of responses by amplitude: responses >2500pA will be APs, while sthr responses are all <300pA in amplitude
# As far as peak-times the distribution looks good: they all fall within 2.5 - 6ms post ttl onset

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 2000]

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# These distributions all look really normal, aside from the fact that the majority of responses seems to have their
# peak at exactly the same time ~4.8ms post ttl. The shortest latency is ~2.5ms, well within reason for being a synaptic response

# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.baselinec < -70],
#                             postttl_t_inms=15,
#                             prettl_t_inms=2,
#                             )
# looks like responses are very similar in amp throughout, but shape may change a bit with holding current change

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 313 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was 0.5ms
# Drug applied: CGP55845;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0717.rtf, cell 1)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0001'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0002'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0003'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
plt.figure()
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# no difference between conditions whatsoever in response amplitudes

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# no difference here either, definitely nothing that looks statistically significant. Possibly the peak-time went up with drug, but it really doesn't look like this would be a significant effect

for drug_condition in drug_conditions:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == drug_condition],
                                postttl_t_inms=15,
                                prettl_t_inms=2,
                                newplot_per_ttlduration=True,
                                plt_title=drug_condition)

# Takeaway based on eyeballing this data: drug makes no difference to response amplitude, maybe to response peak time and probably to baselinec.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

