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

neuron_name = '240509Y'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks like a nice enough recording: cell held at -60mV with -400 - -500pA DC; with sulpiride it spikes in response
# to optostim but not always

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# Cell was held at -70mV for the final recording file, -60mV for the rest.
# Let's see what's up with that:
neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.applied_voltage < -65],
                            postttl_t_inms=30,
                            prettl_t_inms=10,
                            )
# Well. Seems like at -60mV, cell may be spiking most of the time once Sulpiride washed on;
# going down to -70 helps a bit but cell still spiking a lot of the time.

# Let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# This is looking pretty neat: by amplitude, APs are well over 2nA while subthreshold responses are <450pA;
# and response peaks were all measured 2 - 6ms post ttl onset so that's well within range for responses

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 2000]

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# From the distributions, it doesn't look like there are any outliers
neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 3.5],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            )
# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 403 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 1ms;
# Drug applied: Sulpride;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0509.rtf, cell 1)
drug_conditions = ['no drug', 'wash in', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0001'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0002'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0003'), 'drug_condition'] = 'wash out'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0004'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
# At this point, let's first take off responses recorded at -70mV:
ttlonmeasures_sthr_60mV = ttlonmeasures_sthr[(ttlonmeasures_sthr.applied_voltage > -65)]
sns.lmplot(data=ttlonmeasures_sthr_60mV, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr_60mV, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# And let's see also with those:
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# My eye says: no significant differences in response amplitude between conditions;
# the condition that looks the most different from baseline is the washout

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# Doesn't look to me like there are any significant changes here, either.

