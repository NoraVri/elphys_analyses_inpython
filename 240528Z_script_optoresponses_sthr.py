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

neuron_name = '240528Z'
neuron_data = SingleNeuron(neuron_name)

neuron_data.plot_rawdatablocks(segments_overlayed=False)
neuron_data.plot_rawdatablocks(segments_overlayed=True)
# notes on recording quality:
# Looks like a pretty neat and steady recording, with cell needing <100pA to keep -60/-70mV;
# at -60mV it was spiking a lot in response to optoStim
# Also seeing a handful of sizeable spontaneously occurring depolarizations.

# %% getting optoStim response measurements:
neuron_data.get_singlepulse_ttlonmeasures_fromrawdata(response_window_inms=50)
ttlonmeasures = neuron_data.ttlon_measures.copy()

# check and see recording conditions:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
# The first recording block was taken at Vm=-60mV, then holding changed to -70mV for the rest of recordings.

# Let's see some more response parameters:
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# This doesn't look fully sensical: cell is spiking most at more negative holding c (~-120 - -180pA),
# and responses come markedly earlier than at the less negative holding c level (~-80pA).

# Notably, cell starts to spike more as baselinec gets more negative during the first recording block at -60mV;
# changing holding V to -70mV stops spiking, and then baselinec gets a lot less negative again.
for file in ttlonmeasures.file_origin.unique():
    neuron_data.plot_ttlaligned(ttlonmeasures[ttlonmeasures.file_origin == file],
                            postttl_t_inms=25,
                            prettl_t_inms=5,
                            )

# Since the first recording block has mostly spikes, and conditions don't match the rest of recordings, I'm deciding to
# filter out this block:
first_rec_block = ttlonmeasures.file_origin.unique()[0]
ttlonmeasures = ttlonmeasures[~(ttlonmeasures.file_origin == first_rec_block)]

# Now let's see all response parameters together again:
sns.jointplot(data=ttlonmeasures, x='applied_voltage', y='baselinec', hue='file_origin')
ttlonmeasures.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures.hist(column='baselinec_range', bins=200)
# That's better: all responses are subthreshold (~200 - 450pA). I do see baselinec shift markedly during
# the first recording block taken at -70mV, should pay attention to see whether this is drug effect or starts before.
# Response peak times are between 3 and 8ms and distributed in a way that may not be normal - another attention point.

# %% Getting subthreshold responses only:
ttlonmeasures_sthr = ttlonmeasures

# %% examining outliers and excluding bad measurements from the data:
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'response_maxamp', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.plot.scatter('response_maxamp_postttl_t_inms', 'baselinec_range', c='baselinec', colormap='Spectral')
ttlonmeasures_sthr.hist(column='response_maxamp_postttl_t_inms', bins=200)
ttlonmeasures_sthr.hist(column='baselinec_range', bins=200)
# Looks like there aren't really outliers in this data, but I'm still suspicious of this baselinec shift,
# especially since it also seems that more negative baselinec corresponds to earlier response peak times.

for file in ttlonmeasures_sthr.file_origin.unique():
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.file_origin == file],
                            postttl_t_inms=25,
                            prettl_t_inms=5,
                            )

ttlonmeasures_sthr.hist(column='baselinec', bins=200, by='file_origin', sharex=True, sharey=True)
for file in ttlonmeasures_sthr.file_origin.unique():
    ttlonmeasures_sthr[ttlonmeasures_sthr.file_origin == file].plot.scatter(x='segment_idx', y='baselinec', c='response_maxamp')
# I still don't fully like the look of this: baselinec clearly rising steadily over the course of the first recording
# block done at -70mV, and wobbly in weird ways also in the next two. Still, response amplitude variability looks rather
# independent of baselinec, so let's just see what's what without excluding any more data.

# Having looked at all the data, I am convinced that the response peaks were all measured appropriately
# given what's in the raw data.

# This dataset consists of 300 recorded subthreshold responses.

# %% adding optoStim parameters to the dataframe:
# Light stim duration was always 0.5ms;
# Drug applied: Quinpirole;
# Light intensity was always the same (%intensity not noted)

# Adding drug conditions as a column to ttlonmeasures dataframe: (from Notes0528.rtf, cell 2 (-60mV) [the second Cell 2 in these notes])
drug_conditions = ['no drug', 'wash in/with drug', 'with drug', 'wash out']
ttlonmeasures_sthr.loc[:, 'drug_condition'] = 'no drug'
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0011'), 'drug_condition'] = 'wash in/with drug' #!Note: blocks marked as having drug applied start at the time solution is switched, so the first ... segments should be considered 'wash in'.
ttlonmeasures_sthr.loc[ttlonmeasures_sthr.file_origin.str.contains('0012'), 'drug_condition'] = 'with drug'

# plotting a quick overview of the recording conditions:
sns.scatterplot(data=ttlonmeasures_sthr, x='applied_voltage', y='baselinec',
                hue='drug_condition',)

# %% plots: response sensitivity to drug
sns.lmplot(data=ttlonmeasures_sthr, x='baselinec', y='response_maxamp', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp', hue='drug_condition')
# That comes out looking quite clear and neat: response amp decreases with drug application,
# going from ~350pA with to ~300pA without drug.
# Jitter quite large though: whiskers are ~50pA and there's lots of overlap between groups.

sns.lmplot(data=ttlonmeasures_sthr, x='response_maxamp', y='response_maxamp_postttl_t_inms', hue='drug_condition',)
plt.figure()
sns.boxplot(data=ttlonmeasures_sthr, x='ttlon_duration_inms', y='response_maxamp_postttl_t_inms', hue='drug_condition')
# I don't know how or why this comes out looking more significant than the amplitudes-change, but response peaks clearly
# get later with drug application (going from ~4.2 to ~6ms; jitter ~3ms all around).

# %% saving the data: subthreshold responses to optoStim
neuron_data.write_df_tocsv(ttlonmeasures_sthr, 'optostimresponses_sthr')

