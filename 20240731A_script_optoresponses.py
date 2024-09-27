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

neuron_name = '20240731A'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
# neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# recording conditions have clearly deteriorated quite a bit by the end; AP peakV down from +20 to ~-20mV,
# even while it seems like baselineV kept at ~-60mV with -150pA DC throughout.
# Looks like deterioration is fast and sudden starting optoStim_5pct #16 - previous file still had AP peaks >0mV, now suddenly we're down to AP peaking at -25mV.

# %% notes on optoStim experiments:
# neuron_data.get_ttlonmeasures_fromrawdata()
ttlonmeasures = neuron_data.ttlon_measures.copy()
# ttlonmeasures.file_origin.unique()
# ttlonmeasures.ttlon_duration_inms.unique()
ttlonmeasures.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms
# Light intensity was varied (5% in 18 recording files, 100% in 5 others)
# Various levels of holding current applied to change baselineV; looks like recording conditions drifted:
# there's a 5-20mV range of baselineV values at each holding level.



# %%
# Adding drug conditions as a column to ttlonmeasures dataframe (even though no drug applied for this neuron):
drug_conditions = ['no drug']
# ttlonmeasures.loc[:, 'drug_condition'] = 'no drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 100]
# ttlonmeasures.loc[:,'stim_intensity_pct'] = ''
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
# ttlonmeasures.loc[ttlonmeasures.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# Adding holding current as a categories-column to ttlonmeasures dataframe:
holding_current_levels = ['-400pA', '-350pA', '-300pA', '-250pA', '-200pA', '-150pA', '-125pA', '-100pA', '-50pA', '0pA']
# ttlonmeasures['applied_current group'] = pd.cut(ttlonmeasures['applied_current'],
#                                                 bins=[-450, -370, -325, -275, -225, -170, -140, -110, -80, -25, 25],
#                                                 labels=['-400pA', '-350pA', '-300pA', '-250pA', '-200pA', '-150pA', '-125pA', '-100pA', '-50pA', '0pA'])

# Adding baselinev as a categorical variable to ttlonmeasures dataframe by rounding to no decimals:
# baselinev = ttlonmeasures.baselinev
# binned_baselinev = baselinev.round(decimals=0)
# ttlonmeasures.loc[:, 'binned_baselinev'] = binned_baselinev

# neuron_data.ttlon_measures = ttlonmeasures.copy()
# neuron_data.write_results()

# %% filtering for subthreshold responses
# check and see: are APs and subthreshold responses easy to distinguish?
ttlonmeasures.plot.scatter('baselinev', 'response_maxamp')
# interesting: subthreshold responses only when baselineV <-75mV, and even then it's often an AP.
# I'm also seeing small clusters of responses that don't seem to belong: probably they're from recording files
# where conditions were deteriorating. Let's check:
ttlonmeasures[((ttlonmeasures.response_maxamp > 40) &
               (ttlonmeasures.response_maxamp < 72) &
               (ttlonmeasures.baselinev > -82) &
               (ttlonmeasures.baselinev < -64))].file_origin.unique()
# indeed - optoStim_5pct files 14 - 17 (where recordings ended). Excluding these datapoints:
ttlonmeasures_deteriorationexcluded = ttlonmeasures.loc[:189,:]

ttlonmeasures_deteriorationexcluded.plot.scatter('baselinev', 'response_maxamp')
# Good, this looks neat now: a cluster of subthreshold responses at -95 < baselineV < -75, amp ~20-35mV.
# APs occurring at all levels of baselineV, peakVs affected by baselineV so that they are on a line with negative slope.

# Now let's filter down to subthreshold responses:
ttlonmeasures_sthr = ttlonmeasures_deteriorationexcluded[((ttlonmeasures_deteriorationexcluded.response_maxamp < 40) & (ttlonmeasures_deteriorationexcluded.baselinev < -40))]


# %% opto response sensitivity to light intensity & baseline voltage
plt.figure()
sns.lineplot(data=ttlonmeasures_sthr, x='binned_baselinev', y='response_maxamp', hue='stim_intensity_pct')
# not a lot of datapoints to go by - only three subthreshold responses recorded for stim.intensity 100%.
# Going from 100% to 5% stim. intensity response amp goes down by about 10mV to ~25mV.
# No clear relationship between baselineV and response amp, but again, data limited: only 15mV range where subthreshold responses occurred at all.





