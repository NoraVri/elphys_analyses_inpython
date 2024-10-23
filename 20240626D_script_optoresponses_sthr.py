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

neuron_name = '20240626D'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice seal (>GOhm) and patch (@t=78.90s in gapFree_0000).
# Fires off a couple dozen APs before deciding to sit mostly subthreshold at Vm~-47mV without DC.
# Slight drop in Vm towards end of recordings (with sulpiride) and no longer firing spontAPs; still easy to evoke though, and parameters look practically unchanged
#!!Note from recording day: "As I'm switching out the Sulpiride ACSF, I noticed that the regular ACSF looks bad - it's milky and even a little yellow-looking".

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=20)  # re-set from default, see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks very sensical. Looks like responses were picked up mostly neatly, all except two points have latency 2.5 - 16ms.
# By amplitude, there is a clear separation between subthreshold (<16mV) and AP responses (>65mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
#                             postttl_t_inms=100)
# Indeed, these are all APs. The subthreshold responses look mostly good, there's always a clear first peak that decays within 20ms and those two outlier points got mismeasured because of spontaneously occurring depolarizations.
## Re-running get_ttlonmeasures_fromrawdata with 20ms window setting

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 40)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)
# No outliers really:
# subthreshold responses all have latencies between 3.5 and 13ms. The distribution of peak times has a bit of a long tail, but I did not see any bad measurements, that's what the data is like.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 12],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# Having plotted various subsets of the data, I am convinced that at this point there is no reason to exclude any.
ttlonmeasures_sthr = ttlonmeasures_sthr.copy()
# This dataset consists of 316 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Sulpiride;
# Light intensity not noted in file names. Notes from recording day: optoStim 0-7 intensity=5%; 8-15 intensity=50%; 16- intensity=100%
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WithSul'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 50, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = 100
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('optoStim_000[0-7]'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('optoStim_000[8-9]'),'stim_intensity_pct'] = 50
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('optoStim_001[0-5]'),'stim_intensity_pct'] = 50

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition', hue_order=drug_conditions,
                size='stim_intensity_pct', size_order=intensity_levels,
                )
plt.title('recording conditions overview')
# Note: there doesn't seem to be a significant shift in baselineV following drug application;
# still, no subthreshold responses recorded in drug-condition at the most depolarized Vm where response was subthreshold without drug - note from later: that's probably because only at 5% we got subthreshold responses there

# %% plots: response sensitivity to light intensity & baseline voltage
# Light intensity was varied only in the no-drug condition.
# Filtering down the DF for proper comparisons:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
# That looks like there is a systematic increase in response amp with increasing light intensity.
# The increase is ~2-3mV going from each level to the next, and is more pronounced for more hyperpolarized Vm
# at 5% intensity response amp is ~5mV, for 100% it's ~10mV.

# Note on relationship between baselineV and response amp: it looks like it might be there, but it's rather small if not totally flat.

# %% plots: response sensitivity to drug
# drug recordings were all done at 100% intensity. Getting the relevant subset of the DF:
ttlonmeasures_sthr_stim100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]

sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp',
           hue='drug_condition', hue_order=drug_conditions)
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp_postttl_t_inms',
           hue='drug_condition', hue_order=drug_conditions)
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxdvdt',
           hue='drug_condition', hue_order=drug_conditions)

# That looks like a pretty straightforward increase in response amp. with drug, from 9-10mV to 12mV.
