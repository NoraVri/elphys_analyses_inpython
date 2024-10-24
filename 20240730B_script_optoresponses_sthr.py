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

neuron_name = '20240730B'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Nice seal (~2GOhm) and patch (@t=50.78s in gapFree_0000). Cell seems to be spiking with freq.~10Hz while sealing;
# this remains the case after break-in, but looks more like a burst/pause kind of pattern, with APs mostly coming in pairs or triplets.
# Towards the end of recordings (~17min. altogether) AP freq is down to ~8Hz and a lot more regular;
# no obvious deterioration of AP parameters (AHP trough -55 - -60mV, AP peakV >+20mV).
# Cell is held subthreshold @~-60mV with -75pA DC.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=30)  # re-set from default, see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# not really. The histogram of postttl_t is practically flat while mostly occupying the full range of values,
# making it feel like a lot of the 'response peaks' that got picked up are actually kind of random.
# For sure, there are no AP responses.
# Having plotted some of the data, it indeed looks like there isn't much of any response; if there is, the peak occurs within 30ms from the stimulus.
## Re-running get_ttlonmeasures with window set accordingly

# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms > 40],
#                             postttl_t_inms=100)

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon after the stimulus:
# a handful responses got measured at latency <3ms from stimulus; V happens to be going down in stimulus window in these cases.
# Then there's a bit of a gap in the histogram; most responses were measured 4 - 25ms after stimulus.
# On the side of too long after the stimulus:
# None of the responses really look like responses, it's really just noisiness in the traces getting picked up.
# Having plotted a bunch of the data, I am convinced that responses with latency >20ms can be reasonably excluded, too,
# on the grounds that the voltage in those traces keeps increasing (peaks at 20-30ms post ttl get picked up because of noise).

# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms < 3],
#                             postttl_t_inms=150)
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp_postttl_t_inms > 20],
#                             postttl_t_inms=150)
# Whittling down the subthreshold responses DF accordingly:
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms >= 3]
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 20]
# This dataset consists of 16 recorded subthreshold 'responses' (all <1mV amp., in range with noise/spont.activity amplitudes).

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was 1 or 10ms;
# Drug applied: none;
# Light intensity was 5% or 100%
# Same level of holding current applied for all trials

# Adding drug conditions as a column to ttlonmeasures dataframe:
drug_conditions = ['no drug']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'

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
# light stimulus strength increased in two ways: increased intensity (5 to 100%) and duration (1 to 10ms).
sns.lmplot(data=ttlonmeasures_sthr, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           col='ttlon_duration_inms',
           )
# Neither manipulation seems to have had any effect on 'response' - everything that got picked up is <1mV in amplitude.
# no information on response amp relative to baselineV; holding current levels not varied

# My conclusion: this neuron did not respond to the light.

# %% plots: response sensitivity to drug
# no drug recordings performed for this neuron.
# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
