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

neuron_name = '240509Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks like a decent enough recording: cell getting held at -75mV throughout; it's quite wobbly about
# baselineC at first (-200 - -500pA) but then settles in at ~-200pA for most of the recording.
# Doesn't look like there's any spontaneous activity going on, just little bits of noise here and there.

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# weird: points that look like outliers are from the first recording file. Let's see what may be going on with that:
plt.figure()
sns.scatterplot(data=ttlonmeasures[ttlonmeasures.file_origin == '2024_05_09_0005.abf'],
                x='segment_idx', y='response_maxamp', c=ttlonmeasures[ttlonmeasures.file_origin == '2024_05_09_0005.abf'].baselinec)
# Interesting. Response amplitude is gradually going down over the course of this recording file; it stabilizes after
# ~50 segments, but at this point the baselineC needed to keep the voltage gets unstable.

# Let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Looks like there may be an inverse relationship between response amp and peak time: the longer it takes for the
# response to peak, the smaller it is.
# Seems all responses are subthreshold (<400pA), and with peak times 1.5 - 3.5ms post ttl this is looking pretty neat.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# Looking at the data this way, there don't seem to be any outliers.
neuron_data.plot_ttlaligned(ttlonmeasures_sthr,
                            postttl_t_inms=25,
                            prettl_t_inms=5,
                            )
# Indeed, responses all look very vanilla by shape, no reason why peaks shouldn't get picked up appropriately.

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 588 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 0.5ms;
# Drug applied: Sulpride;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0509.rtf, cell 1)
drug_conditions = ['no drug', 'wash in', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0006'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0007'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0008'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0009'), 'drug_condition'] = 'wash out'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0010'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# Looks like amplitude is slightly higher before drug application, though not very significantly - however, given that
# response amp was going down already before drug got applied, I don't think there's any difference really

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# no difference here whatsoever