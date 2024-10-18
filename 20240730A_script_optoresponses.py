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

neuron_name = '20240730A'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice seal (~1.5GOhm) and patch (@t=49.5s in gapFree_0000); cell spiking with freq. just over 20Hz
# and then held subthreshold at -60mV with -75pA DC. After drug application, cell stays at -60mV with -50pA DC.
# Seeing TONS of spontaneously occurring subthreshold depolarizations, some of them huge (up to ~20mV), and some of the time they seem rhythmic.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=150)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# yes, this looks mostly sensical. Looks like responses were always quite neat, all got picked up with peak posttl_t < 7ms.
# By amplitude, there is a clear separation between subthreshold (<40mV) and AP responses (>60mV). Check to see:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 40],
#                             postttl_t_inms=100)
#                             indeed, these are all APs. Notably, no spont.spiking in any of these traces;
#                             even though baselineV goes down <-90mV, APs are regularly evoked by the stimulation.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[(ttlonmeasures.response_maxamp < 40)]
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# No responses got measured too soon after stim.on, latencies are >3ms for all responses.
# On the side of too long after the stimulus:
# No responses were measured anywhere close to the end of the 150ms response window, the longest latencies are <7ms.

# Having plotted various subsets of the data, I am convinced that these are all proper subthreshold responses.
ttlonmeasures_sthr = ttlonmeasures_sthr.copy()
# This dataset consists of 390 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was 1, 0.7 or 0.5ms;
# Drug applied: Quinpirole;
# Light intensity was 5% for all recordings
# Various levels of holding current applied

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug', 'wash in', 'with drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WashIn'), 'drug_condition'] = 'wash in'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('WithQuin'), 'drug_condition'] = 'with drug'

# Adding light intensity as a column to ttlonmeasures dataframe:
intensity_levels = [5]
ttlonmeasures_sthr.loc[:,'stim_intensity_pct'] = 5

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_current', y='baselinev',
                hue='drug_condition',
                style='ttlon_duration_inms',
                )

# Note: this neuron was insanely responsive to the optoStim!! Even at 5% intensity and baselineV <-90mV,
# I got just one or two subthreshold responses for light duration 1 and 0.7ms, respectively (~1 block each)

# %% plots: response sensitivity to light intensity & baseline voltage
# All blocks were recorded with 5% light intensity, and all except 3 responses at light duration 0.5ms.
# Taking the no-drug condition to see how those 3 responses compare to the rest:
ttlonmeasures_sthr_nodrug = ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug']

sns.lmplot(data=ttlonmeasures_sthr_nodrug, x='baselinev', y='response_maxamp',
           hue='ttlon_duration_inms',
           )
# There's no comparison really: those three responses recorded at >0.5ms duration are also more hyperpolarized
# (-95 and -100mV vs -90 - -70mV for responses recorded at 0.5ms stim duration)

# Note on relationship between baselineV and response amp: the distribution of response amps at each baselineV
# (up to ~7mV) is much larger than the effect, but there does seem to be a trend for response amps to be
# ~3mV larger at -90mV than at -70mV (where mean amp is ~17mV)

# %% plots: response sensitivity to drug
# drug recordings were all done with ttl duration 0.5ms. Filtering down the DF accordingly:
ttlonmeasures_sthr_stimhalfms = ttlonmeasures_sthr[ttlonmeasures_sthr.ttlon_duration_inms == 0.5]

sns.lmplot(data=ttlonmeasures_sthr_stimhalfms, x='baselinev', y='response_maxamp', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stimhalfms, x='baselinev', y='response_maxamp_postttl_t_inms', hue='drug_condition')
sns.lmplot(data=ttlonmeasures_sthr_stimhalfms, x='baselinev', y='response_maxdvdt', hue='drug_condition')

neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stimhalfms[ttlonmeasures_sthr_stimhalfms.drug_condition == 'no drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='no drug'
                            )
neuron_data.plot_ttlaligned(ttlonmeasures_sthr_stimhalfms[ttlonmeasures_sthr_stimhalfms.drug_condition == 'with drug'],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            plt_title='with drug'
                            )
# Well that's very interesting. Looks like response amplitude goes down by ~3mV with drug application
# (from ~18mV @baselineV~-70mV w/o drug), but mostly because summation works somehow differently after drug
# (as seen from max.dVdt increase after drug application).
