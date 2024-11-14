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

neuron_name = '240703Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
# notes on recording quality:
# Looks like a mostly nice recording: cell held with ~-150pA to keep baselineV at -70mV, although I do see
# a systematic decrease in the capacitance artefact over the course of recordings (also, hard to say by eye
# what's going on with test pulse amplitude). Also, clamping clearly not ideal: neuron is doing APs in response to
# optostim with ~25% probability towards the end of recordings, and there's a significant shift in baselinec for
# the last few sweeps of optoStim responses

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# that's looking quite alright, except for the handful of points from the final optoStim file where baselineC goes
# from ~-300pA to double that all of a sudden. Filtering those out:
ending_conditions = ((ttlonmeasures.file_origin == '2024_07_03_0005.abf') & (ttlonmeasures.segment_idx >= 92))
ttlonmeasures = ttlonmeasures[~ending_conditions]

# check and see recording conditions again:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# this looks good, whatever drift there is in recording conditions looks insignificant.

# Now let's see more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# Looks like this data needs some more cleaning up: by amplitude, there is a group of responses that are clearly APs
# (amp. >3nA), and there seem to be some outliers among the subthreshold responses that will need to be examined.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 3000]

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# One outlier-point was measured as having ~0amp and postttl t; let's see it:
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms < 1],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# This response seems to be occurring on top of some spontaneous hyperpolarizing event - no real response to be measured
# from the raw data in this trace. Excluding it:
ttlonmeasures_sthr = ttlonmeasures_sthr[~(ttlonmeasures_sthr.response_maxamp_postttl_t_inms < 1)]
# Another outlier point, by amplitude, looks to be an AP occurring kinda randomly:
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp > 800],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# Excluding it:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp < 800]

# Interestingly, there seems to be a grouping of the responses by amp and peak-time: as responses get larger,
# their peak time shifts to be later. Looks to me like all responses are comprised of two events, and the separation
# between them becomes more pronounced; inasmuch as the events are clearly stacked on top of each other, I do think
# they are properly measured like this.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 4],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately.

# This dataset consists of 511 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 0.5ms;
# Drug applied: Sulpride;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0703.rtf, cell 1)
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0002'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0003'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0004'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0005'), 'drug_condition'] = 'wash out'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# my eye says: no significant difference. There's things going on in this data besides drug effect.
# Loads of inter-trial variance going on in every condition, and it seems to only get larger as recordings continue.
# Drug may bring mean amp down by ~50pA (~250pA to start with) but this effect is much smaller than the variance
# from trial to trial (150 - 300pA for no drug and with drug conditions, respectively).
# Also, response amp bounces way up past baseline condition (mean ~250pA) for drug washout condition (mean ~400pA).

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# From looking at this data, I'd say that what's going on is the Vclamp is gradually worsening until it's lost almost
# altogether towards the end of recordings: the second upstroke of the response becomes more and more pronounced,
# shifting both peak amp and time to larger values.

for drug_condition in drug_conditions:
    dc_ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == drug_condition]
    neuron_data.plot_ttlaligned(dc_ttlonmeasures_sthr,
                                postttl_t_inms=15,
                                prettl_t_inms=10,
                                plt_title=drug_condition,
                                )

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
