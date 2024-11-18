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

neuron_name = '240724Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# holding current to keep -60mV looking pretty small (~-150pA) and nice and stable for the most part;
# capacitance artefact looks quite variable though, going down at first and then up again over the course of recordings
# Optostim responses subthreshold for the most part, saw just one AP

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=15)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# I think that looks OK - slight drift down in holding current over the course of recordings, from ~-75 to ~-150pA

# Now let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Looks nice - peaks were all picked up with latency 2.6 - 3.8ms post ttl, and parameter distributions all look rather normal.
# The one AP response is easy to recognize by amplitude (>3500pA, whereas sthr responses are all <650pA).

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 3000]

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)

neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.baselinec > -100],
                            postttl_t_inms=15,
                            prettl_t_inms=2,
                            )
# Looks like responses are all rather similar, and measured properly.

# Having looked at all the recorded responses, I am convinced that the response peaks were all measured appropriately given the raw data.

# This dataset consists of 399 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was 0.5ms
# Drug applied: CGP55845;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0724.rtf, cell 1)
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
# Looks like amp may have gone up a little from ~300 to ~350pA, while baselinec shifted from ~-90 to ~-140pA
# Large variance all around though, changes do not look significant to me.

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')


for drug_condition in drug_conditions:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == drug_condition],
                                postttl_t_inms=15,
                                prettl_t_inms=2,
                                newplot_per_ttlduration=True,
                                plt_title=drug_condition)

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

