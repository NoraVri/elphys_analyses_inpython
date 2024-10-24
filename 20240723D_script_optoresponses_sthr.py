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

neuron_name = '20240723D'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# gapFree_0000 (the first recording file) is a break-in into a dead neuron (confirmed with notes from experiment day).
# Removing:
# neuron_data.rawdata_remove_nonrecordingblock('gapFree_0000.abf')
# neuron_data.write_results()
# Nice seal (just under 2MOhm) and patch (@t=95.87 in gapFree_0001).
# While cell-attached, APfreq looks to be ~7Hz; on break-in, it's ~40Hz. Cell gets held subthreshold ~-60mV with -100pA DC.
# No GF-recording taken after drug application.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=20)  # adjusted from default; see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks mostly sensical. Looks like responses were mostly quite neat: most have latency <15ms, three responses have latency of 150ms.
# By amplitude, there is a clear separation between subthreshold (<11mV) and AP responses (>60mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
#                             postttl_t_inms=100)
# Indeed, these are all APs.
# Next looking at all subthreshold responses, it is clear that the regularly occurring spontaneous depolarizations are
# messing with some of our measurements: the peak of the light response is always within 60ms from the stimulus.
## Re-running get_depolarizingevents accordingly with 60ms window.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 40)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# No responses got measured too soon after stim., the shortest latency is ~3.3ms.
# On the side of too long after the stimulus:
# Looking more closely at the outliers in terms of post_ttl_t, it is clear that these should follow the stimulus
# even more tightly: at the most depolarized potential where we still get subthreshold responses, the first peak is
# within 20ms from the stimulus. Responses occurring at more hyperpolarized potential peak even earlier; the ones
# that get included in this plot have another spont.depol arriving within 10ms, with peak amp. larger than that of
# the light stim response.
## Re-running get-depolarizingevents accordingly with 20ms window.
# There are now just 2 responses with latency >16ms. I think both of these should be excluded: in one trace,
# voltage is continuously rising without a clear peak; in the other, the measured voltage peak is caused by a
# second depolarizing event occurring within a ms from the peak caused by optostim.

# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 10],
#                             postttl_t_inms=100)

# Having plotted various subsets of the data, I am convinced that only those two responses were mismeasured and needs to be excluded.
# Whittling down the DF accordingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 16]
# This dataset consists of 474 recorded subthreshold responses.  !Note: more get excluded because of a change in recording conditions - see below.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: Quinpirole;
# Light intensity was 5, 50 or 100% (varied in without-drug condition only)
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 50, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = ''
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('50p'),'stim_intensity_pct'] = 50
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition',
                size='stim_intensity_pct',
                )
plt.title('recording conditions overview')

# Note: it looks like there is a significant shift in baselineV after drug application.
# Confusingly, it seems to go in both directions: for DC <-150pA, we get higher baselineV with drug; for DC >-100pA, lower.

# check to see: did recording conditions deteriorate, causing this weird effect?
# neuron_data.plot_rawdatablocks('optoStim_100pct_withQuin')
# I don't see anything obvious, but it does feel like spont.depolarizations disappear rather suddenly starting from file optoStim_100pct_withQuinpirole_004.
blocks_for_excluding = neuron_data.get_blocknames(printing='off')[44:50]
ttlonmeasures_sthr_excl = ttlonmeasures_sthr
for block in blocks_for_excluding:
    ttlonmeasures_sthr_excl = ttlonmeasures_sthr_excl[~(ttlonmeasures_sthr_excl.file_origin == block)]
plt.figure()
sns.scatterplot(data=ttlonmeasures_sthr_excl, x='applied_current', y='baselinev',
                hue='drug_condition',
                size='stim_intensity_pct',
                )
plt.title('recording conditions overview - data excluded')
# Yes, this looks more sensical: baselineV change in a single direction, and in line with what happens during wash-in.
# Continuing on without the excluded data:
ttlonmeasures_sthr = ttlonmeasures_sthr_excl

# %% plots: response sensitivity to light intensity & baseline voltage
# All blocks were recorded with light duration 1ms; intensity was varied in non-drug condition only.
# Taking the relevant subset of the DF only:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']
sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )

# There is some sensitivity to light intensity.
# The difference between 5 and 50% does not look at all significant; going from there to 100% the response
# increases by ~1.5mV to be ~4mV on average.

# Note on the relationship between baselineV and response amp.: no clear effect of hyperpolarization
# increasing response amp, lines look mostly flat/responses are more likely to be larger for more depolarized Vm.

# %% plots: response sensitivity to drug
# drug recordings were done for 100% light intensity only. Getting the relevant subset of the DF:
ttlonmeasures_sthr_stim100pct = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]
sns.lmplot(data=ttlonmeasures_sthr_stim100pct, x='baselinev', y='response_maxamp', hue='drug_condition')
plt.title('stim intensity 100%')

# Looks like we get a small but significant increase in response amp. with drug, from ~4 to ~6mV.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

