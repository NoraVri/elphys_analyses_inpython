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

neuron_name = '20240717C'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice seal (just over 2MOhm) and patch (@t=76.38 in gapFree_0000). AP frequency looks somewhat bursty/patterned.
# While cell-attached, AP freq looks to be ~9-15Hz;
# on break-in, AP freq is ~16Hz and falling; continues to be bursty until cell gets held subthreshold @-50mV with -50pA DC.
# Definitely GABAergic neuron though, as seen from high frequency (>80Hz) spiking with depolarizing DC
# At the end of recordings, cell needs no DC to keep subthreshold at -60mV.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=15)  # changed from default; see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks very sensical. Looks like responses were picked up mostly neatly, although there is a long tail in post_ttl_t.
# By amplitude, there is a clear separation between subthreshold (<12mV) and AP responses (>55mV). Check to see:
# # neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
# #                             postttl_t_inms=100)

# Indeed, these are all APs.
# Next looking at all subthreshold responses, at first glance it is clear that some got mismeasured because they have spontaneously occurring depolarizing depolarizing events soon after them; in general, it looks like light response peaks all occur within 15ms of the ttlON.
## Re-running get_ttlonmeasures_fromrawdata with 15ms window

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 40)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# No responses got measured too soon after stim., the shortest latency is ~2.7ms.
# On the side of too long after the stimulus:
# As always, the postttl_t histogram has a bit of a long tail, and honestly it's hard to tell sometimes whether
# something happens in response to the ttl or spontaneously. However, I think I can safely say that at
# latencies >9ms, we get only strange responses that get to be excluded.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 9],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# And having plotted various subsets of the data, I am convinced that those are the only subthreshold responses that should be excluded.
# Whittling down the DF accordingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 9]
# This dataset consists of 397 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Quinpirole;
# Light intensity was mostly 100%, 3 blocks each at 5 and 50% intensity in no-drug condition only
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashOut'), 'drug_condition'] = 'wash out'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 50, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = ''
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('50p'),'stim_intensity_pct'] = 50
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition', hue_order=drug_conditions,
                size='stim_intensity_pct',
                )
plt.title('recording conditions overview')
# Note: it looks like there may be a slight shift down in baselineV with drug application (~5mV);
# but it also looks as though Vm may have been already falling steadily before drug was applied,
# and continues to do so as drug is washed out.

# %% plots: response sensitivity to light intensity & baseline voltage
# Light intensity was varied only in the no-drug condition.
# Filtering down the DF for proper comparisons:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
# That looks like there is a systematic increase in response amp with increasing light intensity.
# The changes are small, but look like they may be significant nonetheless.

# Note on relationship between baselineV and response amp: it looks like it might be there,
# but being quite small to begin with and having a lot of jitter it looks not so significant.

# %% plots: response sensitivity to drug
# drug recordings were all done at 100% intensity. Getting the relevant subset of the DF:
ttlonmeasures_sthr_stim100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]

sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp',
           hue='drug_condition', hue_order=drug_conditions)
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp_postttl_t_inms',
           hue='drug_condition', hue_order=drug_conditions)
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxdvdt',
           hue='drug_condition', hue_order=drug_conditions)

# That looks like a slight but significant increase in response amp with drug, from ~2 to ~3.5mV.
# Not sure what's up with response looking to continue increasing with washout though.
drug_conditions = ['no drug', 'with drug', 'wash out']
for condition in drug_conditions:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == condition],
                                postttl_t_inms=150,
                                prettl_t_inms=25,
                                plt_title=condition,
                                plotlims=[-2, 8], color_lims=[-85, -58]
                                )

# It looks like quinpirole application also affected the frequency and amplitude of spontaneously occurring
# depolarizations - they seem a lot more frequent in the drug condition than in no-drug or washout.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

