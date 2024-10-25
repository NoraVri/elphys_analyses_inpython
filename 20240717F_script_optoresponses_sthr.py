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

neuron_name = '20240717F'
neuron_data = SingleNeuron(neuron_name)
neuron_data.get_recordingblocks_index()

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Great seal (>2GOhm) and patch (@t=42.20 in gapFree_0000). Spiking spontaneously but with ~1Hz freq.tops,
# taking frequent pauses when sitting at ~-40mV w/oDC, and quickly reaches depol.block - this is a dopaminergic neuron.

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=30)  # adjusted from default - see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# Just two blocks of optostim recordings for this neuron, and that's because there's no response to be seen really.
neuron_data.plot_ttlaligned(ttlonmeasures,
                            prettl_t_inms=25,
                            postttl_t_inms=150)
# The default 150ms response window picks up a couple of spont.APs awkwardly; by setting the window to 30ms we avoid that.
# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures
# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)
# First, on the side of too soon after the stimulus:
# there are two 'responses' with latency <2ms (and then the next soonest one is >5ms).
# those should definitely be excluded for just being bits of noise.
# On the side of too long after the stimulus:
# There are five points that get measured at the end of the window where V still increasing (spont. AP upslope),
# those should definitely be excluded, too.
neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms > 29.6],
                            postttl_t_inms=150,
                            prettl_t_inms=25,
                            )

ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms >= 2]
ttlonmeasures_sthr = ttlonmeasures_sthr[ttlonmeasures_sthr.response_maxamp_postttl_t_inms <= 29]
# This dataset consists of 14 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms;
# Drug applied: none;
# Light intensity was 5 or 100% (one block each)
# Various levels of holding current applied but not by much

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
# light stimulus strength increased from 5 to 100%.
sns.lmplot(data=ttlonmeasures_sthr, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )

neuron_data.plot_ttlaligned(ttlonmeasures,
                            prettl_t_inms=5,
                            postttl_t_inms=30)

# Everything that got picked up is <1mV in amplitude.
# no information on response amp relative to baselineV; holding current levels not varied nearly enough

# My conclusion: this neuron did not respond to the light.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
