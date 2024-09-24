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

neuron_name = '20240731C'
neuron_data = SingleNeuron(neuron_name)
# neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
# neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')

# Very nice sealing and break-in (@t=77.373s in gapFree_0000) while neuron spiking with freq just below 40Hz.
# AP peakV ~+20mV, AHPmin ~-47mV initially, keeps at ~-70mV w/ -100pA DC;
# After optoStim experiments, holding increased a bit to -150pA to keep ~-70mV and AP parameters look practically unchanged.
# Active properties do seem to have deteriorated after longPulse experiments, will have to pay attention to that in analyses.

# %% notes on optoStim experiments:
# neuron_data.get_ttlonmeasures_fromrawdata()
ttlonmeasures = neuron_data.ttlon_measures.copy()
# ttlon_measures.file_origin.unique()
# ttlon_measures.ttlon_duration_inms.unique()
# ttlonmeasures.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Quinpirole;
# Light intensity was varied (5, 50 and 100%) in no-drug condition only;
# Various levels of holding current applied to change baselineV; looks like recording conditions drifted:
# there's a 10-20mV range of baselineV values at each holding level.


# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
# ttlonmeasures.loc[:, 'drug_condition'] = 'no drug'
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 50, 100]
# ttlonmeasures.loc[:,'stim_intensity_pct'] = ''
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('50p'),'stim_intensity_pct'] = 50
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# Adding holding current as a categories-column to ttlonmeasures dataframe:
holding_current_levels = ['-250pA', '-200pA', '-150pA', '-125pA', '-100pA', '-50pA']
# ttlonmeasures['applied_current group'] = pd.cut(ttlonmeasures['applied_current'],
#                                                 bins=[-260, -220, -175, -140, -110, -75, -25],
#                                                 labels=['-250pA', '-200pA', '-150pA', '-125pA', '-100pA', '-50pA'])

# Adding baselinev as a categorical variable to ttlonmeasures dataframe by rounding to no decimals:
# baselinev = ttlonmeasures.baselinev
# binned_baselinev = baselinev.round(decimals=0)
# ttlonmeasures.loc[:, 'binned_baselinev'] = binned_baselinev

# Seeing whether drug and no-drug conditions are comparable in terms of holding current/baselineV relationship:
plt.figure()
sns.boxplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
# plt.figure()
sns.stripplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
# conclusion: not really... Seems holding DC drifted during wash-in of drug: -200pA with drug has same avg. baselineV as -150pA without drug.

# neuron_data.ttlon_measures = ttlonmeasures.copy()
# neuron_data.write_results()

# %% filtering for subthreshold responses
# check and see: are APs and subthreshold responses easy to distinguish?
# ttlonmeasures.plot.scatter('baselinev', 'response_maxamp')
# yes they are: subthreshold responses are all <20mV, APs all 40mV or more in amp.
# filtering out suprathreshold responses:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 20]


# %% opto response sensitivity to light intensity
# getting ttlonmeasures_df for non-drug runs only:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[(ttlonmeasures_sthr.drug_condition == 'no drug')]
# plotting raw data traces: responses to light at each intensity level
# for level in intensity_levels:
#     ttlonmeasures_nodrug_atlevel = ttlonmeasures_sthr_nodrug[ttlonmeasures_sthr_nodrug.stim_intensity_pct == level]
#     neuron_data.plot_ttlaligned(ttlonmeasures_nodrug_atlevel, plt_title=('intensity=' + str(level)),
#                                 prettl_t_inms=5, postttl_t_inms=70,
#                                 color_lims=[-90, -55],
#                                 plotlims=[-1, 10]
#                                 )
# making a boxplot of response amplitudes by light intensity levels:
plt.figure()
sns.stripplot(data=ttlonmeasures_sthr_nodrug, x='applied_current group', y='response_maxamp', hue='stim_intensity_pct', order=holding_current_levels, hue_order=intensity_levels)
sns.boxplot(data=ttlonmeasures_sthr_nodrug, x='applied_current group', y='response_maxamp', hue='stim_intensity_pct', order=holding_current_levels, hue_order=intensity_levels, fill=False)
plt.title('response amplitude by stimulus intensity (no drug applied)')
# opto response amplitude clearly increases with stim.intensity,
# although for 50 and 100% intensity this is obvious only with strong hyperpolarization (-200pA)

# %% opto response sensitivity to drug
# opto experiments were all carried out at 100% light intensity. Whittling down the df to reflect this:
ttlonmeasures_sthr_100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]

# plotting raw data traces: responses to light in each drug condition
# for condition in drug_conditions:
#     ttlonmeasures_sthr_100pct_incondition = ttlonmeasures_sthr_100pct[ttlonmeasures_sthr_100pct.drug_condition == condition]
#     neuron_data.plot_ttlaligned(ttlonmeasures_sthr_100pct_incondition, plt_title=condition,
#                                 prettl_t_inms=5, postttl_t_inms=70,
#                                 color_lims=[-90, -55],
#                                 plotlims=[-1, 12]
#                                 )

# plotting response amplitudes by drug conditions & baselineV/holding level:
plt.figure()
sns.stripplot(data=ttlonmeasures_sthr_100pct, x='drug_condition', y='response_maxamp', hue='applied_current group', order=drug_conditions, hue_order=holding_current_levels)
sns.boxplot(data=ttlonmeasures_sthr_100pct, x='drug_condition', y='response_maxamp', hue='applied_current group', order=drug_conditions, hue_order=holding_current_levels)

plt.figure()
sns.scatterplot(data=ttlonmeasures_sthr_100pct, x='baselinev', y='response_maxamp', hue='drug_condition')
sns.lineplot(data=ttlonmeasures_sthr_100pct, x='binned_baselinev', y='response_maxamp', hue='drug_condition')
# from the lineplot, it seems pretty clear that response amplitude goes up by ~2mV with drug (from 6 to 8mV on average).
# No clear relationship between baselineV and response amplitude, regardless of drug condition