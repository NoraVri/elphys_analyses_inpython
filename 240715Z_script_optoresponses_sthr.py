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

neuron_name = '240715Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
# notes on recording quality:
# This neuron is being all sorts of super active while pretending to stay clamped at -70mV with ~-700pA DC.
# APs seem to induce currents >10nA, and get more frequent towards the end until cell is totally lost
# for last 2/3 of final recording file (as seen by sudden large increase in -DC to hold -70mV)

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=15)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# yes, there's clearly that dropoff happening during the final recording file. Filtering out those last points:
ending_conditions = ((ttlonmeasures.file_origin == '2024_07_15_0004.abf') & (ttlonmeasures.segment_idx >= 17))
ttlonmeasures = ttlonmeasures[~ending_conditions]

# check and see recording conditions again:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# This looks better, though still not ideal: holding current level is getting less hyperpolarized over time,
# going from ~-900pA initially to ~-500pA towards the end of recordings. Since it happens so gradually, there's really no responses to filter out that would improve on the measurement

# Now let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Looks like (sthr) responses always occur well within 15ms from TTL on, while 'responses'
# occurring 30-150ms post TTL are APs (amp 4 - 11nA). Resetting response window will help with that some
## Re-running get_singlepulse_ttlonmeasures_fromrawdata with 15ms response window
# That looks much better - response peaks were all measured as being <10ms from TTL on, indicating there was always
# a peak to be found well within 15ms from TTL onset.

# Looks like quite a number of the measured responses were APs really - they're all >3nA,
# while sthr responses are all <650pA.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 3000]

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# There's one point that's lying far out from all the others by baselinec_range:
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.baselinec_range > 150],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# Indeed, the TTL here lands on something else depolarizing happening spontaneously, causing baseline to be
# impossible to measure properly. Filtering out this point:
ttlonmeasures_sthr = ttlonmeasures_sthr[~(ttlonmeasures_sthr.baselinec_range > 150)]

# The distribution of peak times looks rather interesting: like there are two main peaks (at 2 and 4ms) when
# response amp is generally low (<300pA), and one main peak (~3ms) when responses amp is large (up to 600pA).
# Holding current is also drastically different in these conditions (-500 to -1000pA, respectively).
# The histogram of response peak times does have a bit of a long tail: most responses occur within 4ms from TTL on,
# but there's a handful that occur 5 - 10ms post.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 5], #4
#                             postttl_t_inms=15,
#                             prettl_t_inms=2,
#                             )
# Yes, these are later peaks of multi-peaked responses, but they are the largest peak so I'm gonna say they're measured correctly.

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 389 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was 0.75ms, except during baseline block where it was 0.5ms;
# Drug applied: CGP55845;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0715.rtf, cell 1)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug',]
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0002'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0003'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0004'), 'drug_condition'] = 'with drug'

# plotting a quick overview of the recording conditions:
plt.figure()
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)
# Note: holding current going from -1000 to -500pA seems to follow drug application.

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# Looks like there may be an ever so slight increase in response amplitude,
# doesn't look to me like it would be significant at all.

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')

for drug_condition in drug_conditions:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == drug_condition],
                                postttl_t_inms=15,
                                prettl_t_inms=2,
                                newplot_per_ttlduration=True,
                                plt_title=drug_condition)
# Weird things are happening in this recording. For one, light stim is 0.5ms to begin with,
# and increasing it to 0.75ms seems to decrease response amp.
# And although response peak times on average do not appear to be different between drug/no drug conditions,
# the scatter shows that with drug, there is more likely to be an early response peak large enough to be the main peak
# at ~2.2ms post TTL on, whereas usually the response peaks ~3.5ms post TTL.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

