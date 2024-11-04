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
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice sealing (just under 2GOhm) and break-in (@t=85.415s in gapFree_0000) while neuron spiking with freq.<2Hz.
# AP peakV and AHP vary with applied current, got just a handful spont.ones early on during recording then silent.
# Keeps ~-60mV with -150pA DC; after optoStim experiments, no holding gives baselineV ~-55.
# Looks like dopaminergic neuron from AP freq.&shape, and depolarization block hit early in longPulse experiments

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=25)  # re-set from default, see notes below (in 'examining outliers')
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks mostly sensical.
# All responses are subthreshold, reaching a maximum amplitude of 3mV.
# No response peaks were measured at the very end of the chosen 150ms response window; two at the end of 25ms response window.
# The histogram of response times looks rather interesting, with multiple distinct peaks in the range <20ms.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# There's one response that's measured right at the start of the search window, and registers as having no amplitude (because it's just a noisy-looking trace without a clear response).
# On the side of too long after the stimulus:
# It looks to me that any 'response' measured more than 20ms post ttl onset is really just noise or a
# spontaneous depolarization - in fact, by 20ms some responses are on their second or third peak already, definitely
# the first peak of the response occurs within 25ms from the stimulus.
## Re-running get_ttlonmeasures_fromrawdata with 25ms response window.
# There are now just two responses that got measured as having their peak at the very end of the search window;
# these are both <1mV in amplitude and noisy, I feel OK excluding them from the dataset for being mismeasurements.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms < 1],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 24],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# Having plotted various subsets of the data, I am convinced that response peak times up to 25ms reflect real response peaks;
# !! However, it does also look like responses may regularly have multiple peaks, and it'll take some paying attention to ensure that comparisons are all fair.
# Whittling down the subthreshold responses DF accordingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms >= 1]
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 24]
# This dataset consists of 546 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was 1 or 10ms;
# Drug applied: Quinpirole;
# Light intensity 5% was used in one block; all others recorded at 100% intensity
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('withQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5, 100]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = ''
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('5p'),'stim_intensity_pct'] = 5
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('100p'),'stim_intensity_pct'] = 100

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition',
                size='stim_intensity_pct',
                style='ttlon_duration_inms')

# %% plots: response sensitivity to light intensity & baseline voltage
# light intensity was varied in no-drug condition only. Getting the relevant subset of the dataframe:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']

sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='ttlon_duration_inms',
           col='stim_intensity_pct',
           )
# insufficient data to make proper comparison; responses for 1ms light duration are few and up to 1.5mV max.amp.

# Note on relationship between response amp and baselineV: seems like it might be there, but small:
# going from 0.5 to 1.5mV when hyperpolarizing from -55 to -80mV
# %% plots: response sensitivity to drug
# drug recordings were done with 100% light intensity only. Getting the relevant subset of the dataframe:
ttlonmeasures_sthr_maxintensity = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100]
sns.lmplot(data=ttlonmeasures_sthr_maxintensity, x='baselinev', y='response_maxamp', hue='drug_condition',
           col='ttlon_duration_inms')
# no proper comparison to be made for 1ms ttl: without drug, only one baselinev level tested

# next splitting out by ttlon_duration:
ttlonmeasures_sthr_maxintensity_10ms = ttlonmeasures_sthr_maxintensity[ttlonmeasures_sthr_maxintensity.ttlon_duration_inms == 10]
sns.lmplot(data=ttlonmeasures_sthr_maxintensity_10ms, x='baselinev', y='response_maxamp', hue='drug_condition',)
sns.lmplot(data=ttlonmeasures_sthr_maxintensity_10ms, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_maxintensity_10ms, x='baselinev', y='response_maxdvdt', hue='drug_condition')
# To me, what this data says is that the properties of the synapses getting the optoStim input did not change
# due to the drug; whatever small differences there seem to be between drug and no-drug conditions are because of
# the underlying baseline voltage change that occurred during drug application.
# There may be some interesting stuff in there regarding single and double-peaked responses

for drug_condition in drug_conditions:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr_maxintensity[ttlonmeasures_sthr_maxintensity.drug_condition == drug_condition],
                            postttl_t_inms=75,
                            prettl_t_inms=25,
                            newplot_per_ttlduration=True,
                            plt_title=drug_condition
                            )
# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
