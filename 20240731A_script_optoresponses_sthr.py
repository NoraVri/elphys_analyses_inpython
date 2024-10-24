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

# notes on recording quality: checking out gapFree recordings
neuron_data.plot_rawdatablocks('gapFree', time_axis_unit='s')
# Neat seal (>GOhm) and patch (@t=127.94s in gapFree_0001.abf) while neuron seems to be spiking at freq.~50Hz;
# spiking with freq.~60Hz on break-in, held subthreshold at ~-65mV with -125pA DC.
# recording conditions have clearly deteriorated quite a bit by the end; AP peakV down from +20 to ~-20mV,
# even while it seems like baselineV mostly kept at ~-60mV with -150pA DC throughout.
# Looks like deterioration is fast and sudden starting optoStim_5pct #16 - previous file still had AP peaks >0mV, now suddenly we're down to AP peaking at -25mV.
# Excluding the last three recording files accordingly:
# neuron_data.rawdata_remove_nonrecordingblock('optoStim_5pct_0016.abf')
# neuron_data.rawdata_remove_nonrecordingblock('optoStim_5pct_0017.abf')
# neuron_data.rawdata_remove_nonrecordingblock('gapFree_0002.abf')
# neuron_data.write_results()

# %% getting optoStim response measurements:
neuron_data.get_ttlonmeasures_fromrawdata(response_window_inms=40)  # re-set from default, see notes below
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see response_maxamp_postttl_t_inms - does it make sense?
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinev_range', bins=200)
# It mostly makes sense, given that APs are probably messing up some of these measurements. From these plots,
# it is clear that subthreshold responses always peak well within 20ms from stimulus onset, as do most APs.
## Re-running get_ttlonmeasures with 40ms timewindow
# yes, that seems to have taken care of most of the ambiguity.
# By amplitude, it seems pretty clear that responses with amp>60mV are APs, and responses with amp<35mV are subthreshold;
# and then there are a few that fall in between.
# It's also clear that some traces are messed up because their baselineV got measured on an AP:
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.baselinev_range > 50],
#                             postttl_t_inms=100)
ttlonmeasures = ttlonmeasures[ttlonmeasures.baselinev_range < 50]
# This gets rid of those in-between amp datapoints.
# neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.response_maxamp > 50],
#                             postttl_t_inms=100)
#                             Indeed, these are all APs, and amp<50mV are all subthreshold responses.
# No response peaks were measured at either edge of the search window, and the long tail of the peak times distribution
# looks accurate given the data.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures[ttlonmeasures.response_maxamp < 50]

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinev', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinev_range', c='baselinev', colormap='Spectral')

ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinev_range', bins=200)

# First, on the side of too soon or too long after the stimulus: no responses that got picked up badly because of this.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr,
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# In fact, as much as the distributions look like they have a couple of outliers in them, it looks to me that they are
# correct given the raw data.
# There is one datapoint with baselinev_range ~1mV; however, with amp~25mV this slight offset in the baselineV
# measurement does not seem worth excluding this datapoint over.
# neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.baselinev_range > 0.5],
#                             postttl_t_inms=150,
#                             prettl_t_inms=25,
#                             )
# Having plotted various subsets of the data, I am convinced that the extracted parameters reflect the responses accurately.
# This dataset consists of 80 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# First, getting the notes on experiments performed on this neuron:
print(ttlonmeasures_sthr.file_origin.unique())
print(ttlonmeasures_sthr.ttlon_duration_inms.unique())
ttlonmeasures_sthr.plot.scatter(x='applied_current', y='baselinev')

# Light stim duration was always 1ms
# Drug applied: none
# Light intensity was varied (100% for one block, 5% in all others)
# Various levels of holding current applied

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
# no drug applied in this neuron, no need to select subset of the DF
sns.lmplot(data=ttlonmeasures_sthr, x='baselinev', y='response_maxamp',
           hue='stim_intensity_pct',
           )
# Only 3 subthreshold responses recorded at 100%, at baselineV <-90mV; the rest must be all APs.
# The relationship between baselineV and response amp. looks mostly flat to me, ~24mV at -95<baselineV<-75

# %% plots: response sensitivity to drug
# No drug effect recorded in this neuron because it died suddenly before I could get to it.

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')
