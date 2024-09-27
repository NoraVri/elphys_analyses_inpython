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

neuron_name = '20240730D'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Pretty strange recording: neat sealing (~4GOhm) and break-in, yet AP peakVs highly variable from the start
# AP freq is high yet irregular (that is: intervals between spont.APs usually very short, but kinda bursty).
# Needs - 300pA to keep from spontaneously spiking at ~-50mV to start with; by the end of recordings -250pA keeps -60mV.

# %% notes on optoStim experiments:
# neuron_data.get_ttlonmeasures_fromrawdata()
ttlonmeasures = neuron_data.ttlon_measures.copy()
# ttlonmeasures.file_origin.unique()
# ttlonmeasures.ttlon_duration_inms.unique()
# ttlonmeasures.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was varied (1, 2, 5 ms)
# Light intensity was not varied; 100% all around
# Various levels of holding current applied to change baselineV.
# Looks like recording conditions drifted: there are wide ranges of baselineV values at each holding level, sometimes even multiple clusters.

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
# ttlonmeasures.loc[:, 'drug_condition'] = 'no drug'
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [100]
# ttlonmeasures.loc[:,'stim_intensity_pct'] = ''
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# Adding holding current as a categories-column to ttlonmeasures dataframe:
# Since there are a lot of levels, I won't enter the groups manually; using quicker grouping instead:
holding_currents_series = ttlonmeasures.applied_current
holding_currents_rounded_series = (holding_currents_series / 10).round(decimals=0) * 10
# ttlonmeasures.loc[:, 'applied_current group'] = holding_currents_rounded_series
holding_current_levels = holding_currents_rounded_series.unique().tolist()
holding_current_levels.sort()

# Adding baselinev as a categorical variable to ttlonmeasures dataframe by rounding to no decimals:
# baselinev = ttlonmeasures.baselinev
# binned_baselinev = baselinev.round(decimals=0)
# ttlonmeasures.loc[:, 'binned_baselinev'] = binned_baselinev


# Seeing whether drug and no-drug conditions are comparable in terms of holding current/baselineV relationship:
plt.figure()
sns.boxplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
plt.figure()
sns.stripplot(data=ttlonmeasures, x='applied_current group', y='baselinev', hue='drug_condition', order=holding_current_levels)
# conclusion: Looks like baselineV comes way down with quinpirole application, by about 20mV.

