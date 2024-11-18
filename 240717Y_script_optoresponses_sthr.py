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

neuron_name = '240717Y'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
# notes on recording quality:
# Looking very nice and stable on the whole, cell held with ~-100pA to keep -60mV pretty much throughout

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=15)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# Indeed that's looking neat: baselinec drifted from ~-90 to ~-130pA over the course of recordings, but even that may have more to do with drug application than any other change in recording conditions

# Now let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Response peaks were all measured <10ms post ttl, and looks like they were all subthreshold (max.amp <200pA)

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# These distributions all look really normal, aside from the fact that the majority of responses seems to have their
# peak at exactly the same time ~4.8ms post ttl. The shortest latency is ~3ms, well within reason for being a synaptic response

# neuron_data.plot_ttlaligned(ttlonmeasures_sthr,
#                             postttl_t_inms=15,
#                             prettl_t_inms=2,
#                             )

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 400 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was 0.5ms;
# Drug applied: CGP55845;
# Light intensity was always the same (%intensity =10 throughout - ?)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0717.rtf, cell 2)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0010'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0011'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0012'), 'drug_condition'] = 'wash out'

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
# no difference here either, definitely nothing that looks statistically significant. Possibly the peak-time variance is higher with drug, but not by much and mean is exactly the same.

for drug_condition in drug_conditions:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == drug_condition],
                                postttl_t_inms=15,
                                prettl_t_inms=2,
                                newplot_per_ttlduration=True,
                                plt_title=drug_condition)

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
