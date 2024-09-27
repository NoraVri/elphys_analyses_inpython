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

neuron_name = '20240731B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
# neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice sealing (just under 2GOhm) and break-in (@t=85.415s in gapFree_0000) while neuron spiking with freq.<2mV.
# AP peakV and AHP vary with applied current, got just a handful spont.ones early on during recording then silent.
# Keeps ~-60mV with -150pA DC; after optoStim experiments, no holding gives baselineV ~-55.
# Looks like dopaminergic neuron from AP freq.&shape, and depolarization block hit early in longPulse experiments

# %% notes on optoStim experiments:
# neuron_data.get_ttlonmeasures_fromrawdata()
ttlonmeasures = neuron_data.ttlon_measures.copy()
# ttlonmeasures.file_origin.unique()
# ttlonmeasures.ttlon_duration_inms.unique()
# ttlonmeasures.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was varied (1, 10 ms)
# Light intensity was varied (5% in one file, 100% in all 54 others)
# Various levels of holding current applied to change baselineV; looks like recording conditions drifted:
# there's a 5-25mV range of baselineV values at each holding level.


# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
# ttlonmeasures.loc[:, 'drug_condition'] = 'no drug'
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 100]
# ttlonmeasures.loc[:,'stim_intensity_pct'] = ''
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# Adding holding current as a categories-column to ttlonmeasures dataframe:
holding_current_levels = ['-400pA', '-300pA', '-250pA', '-200pA', '-150pA', '-100pA', '-50pA', '0pA']
# ttlonmeasures['applied_current group'] = pd.cut(ttlonmeasures['applied_current'],
#                                                 bins=[-450, -350, -275, -225, -170, -120, -80, -25, 25],
#                                                 labels=['-400pA', '-300pA', '-250pA', '-200pA', '-150pA', '-100pA', '-50pA', '0pA'])

# Adding baselinev as a categorical variable to ttlonmeasures dataframe by rounding to no decimals:
# baselinev = ttlonmeasures.baselinev
# binned_baselinev = baselinev.round(decimals=0)
# ttlonmeasures.loc[:, 'binned_baselinev'] = binned_baselinev


# Seeing whether drug and no-drug conditions are comparable in terms of holding current/baselineV relationship:
plt.figure()
sns.boxplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
plt.figure()
sns.stripplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
# conclusion: nope, not at all: looks like baselineV shifts down by 10mV while drug getting applied and stays there

# neuron_data.ttlon_measures = ttlonmeasures.copy()
# neuron_data.write_results()

# %% filtering for subthreshold responses
# check and see: are APs and subthreshold responses easy to distinguish?
# ttlonmeasures.plot.scatter('baselinev', 'response_maxamp')
# No APs in the light responses: the largest one has amp just over 3mV
ttlonmeasures_sthr = ttlonmeasures

# %% opto response sensitivity to light intensity & baseline voltage
# getting ttlonmeasures_df for non-drug runs only:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[(ttlonmeasures_sthr.drug_condition == 'no drug')]

# plotting raw data traces: responses to light at each intensity level & ttl duration
# for level in intensity_levels:
#     ttlonmeasures_nodrug_atlevel = ttlonmeasures_sthr_nodrug[ttlonmeasures_sthr_nodrug.stim_intensity_pct == level]
#     neuron_data.plot_ttlaligned(ttlonmeasures_nodrug_atlevel, plt_title=('intensity=' + str(level)),
#                                 newplot_per_ttlduration=True,
#                                 newplot_per_block=True,
#                                 prettl_t_inms=5, postttl_t_inms=70,
#                                 # color_lims=[-90, -55],
#                                 # plotlims=[-1, 10]
#                                 )
# three conditions:
# 5% intensity/1ms - response barely even rises above the noise, if at all.
# 100% intensity/1ms - largest response just over 1mV in amplitude; still no clearly distinguishable response in most traces
# 100% intensity/10ms - largest response ~3mV in amplitude; lots (if not most) of the responses appear to have multiple peaks.
# They may as well be GJ responses

# comparing 5% and 100% intensity - getting only blocks where ttl duration is 1ms:
ttlonmeasures_sthr_nodrug_1ms = ttlonmeasures_sthr_nodrug[ttlonmeasures_sthr_nodrug.ttlon_duration_inms == 1]
plt.figure()
sns.stripplot(data=ttlonmeasures_sthr_nodrug_1ms, x='applied_current group', y='response_maxamp', hue='stim_intensity_pct', order=holding_current_levels, hue_order=intensity_levels)
sns.boxplot(data=ttlonmeasures_sthr_nodrug_1ms, x='applied_current group', y='response_maxamp', hue='stim_intensity_pct', order=holding_current_levels, hue_order=intensity_levels, fill=False)
plt.title('response amplitude by stimulus intensity (no drug applied)')

# comparing 1ms and 10ms light durations - getting only blocks where ttl intensity is 100%:
ttlonmeasures_sthr_nodrug_100pct = ttlonmeasures_sthr_nodrug[ttlonmeasures_sthr_nodrug.stim_intensity_pct == 100]
plt.figure()
sns.stripplot(data=ttlonmeasures_sthr_nodrug_100pct, x='applied_current group', y='response_maxamp', hue='ttlon_duration_inms', order=holding_current_levels, )
sns.boxplot(data=ttlonmeasures_sthr_nodrug_100pct, x='applied_current group', y='response_maxamp', hue='ttlon_duration_inms', order=holding_current_levels, fill=False)
plt.title('response amplitude by stimulus duration (no drug applied)')

# not much to compare: the 1ms stimulus just doesn't do much towards generating a response.
# We do have some indication here that the response is synaptic: looks like the amplitude goes up significantly for increasing hyperpolarization.
plt.figure()
sns.lineplot(data=ttlonmeasures_sthr_nodrug_100pct, x='binned_baselinev', y='response_maxamp',
             # hue='applied_current group'
             )

# %% opto response sensitivity to drug
# opto experiments were all carried out at 100% light intensity; mostly with 10ms light duration
ttlonmeasures_sthr_100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]

# plotting raw data traces: responses to light in each drug condition
# for condition in drug_conditions:
#     ttlonmeasures_sthr_100pct_incondition = ttlonmeasures_sthr_100pct[ttlonmeasures_sthr_100pct.drug_condition == condition]
#     neuron_data.plot_ttlaligned(ttlonmeasures_sthr_100pct_incondition, plt_title=condition,
#                                 newplot_per_ttlduration=True,
#                                 prettl_t_inms=5, postttl_t_inms=70,
#                                 color_lims=[-90, -55],
#                                 plotlims=[-1.5, 4]
#                                 )

# plotting comparisons: response amplitudes by drug conditions & baselineV, split out by ttl duration
# for duration in ttlonmeasures_sthr_100pct.ttlon_duration_inms.unique():
#     ttlonmeasures_sthr_100pct_atduration = ttlonmeasures_sthr_100pct[ttlonmeasures_sthr_100pct.ttlon_duration_inms == duration]
#     plt.figure()
#     plt.title('light duration = ' + str(duration))
#     sns.scatterplot(data=ttlonmeasures_sthr_100pct_atduration, x='baselinev', y='response_maxamp', hue='drug_condition')
#     sns.lineplot(data=ttlonmeasures_sthr_100pct_atduration, x='binned_baselinev', y='response_maxamp', hue='drug_condition')
# response is small to begin with, but does seem to get significantly even smaller upon drug application
# relationship between baselineV and response amp seems to get lost with drug:
ttlonmeasures_sthr_100pct_10ms = ttlonmeasures_sthr_100pct[ttlonmeasures_sthr_100pct.ttlon_duration_inms == 10]
plt.figure()
sns.scatterplot(data=ttlonmeasures_sthr_100pct_10ms, x='baselinev', y='response_maxamp',
             hue='drug_condition'
             )
sns.lineplot(data=ttlonmeasures_sthr_100pct_10ms, x='binned_baselinev', y='response_maxamp',
             hue='drug_condition'
             )
