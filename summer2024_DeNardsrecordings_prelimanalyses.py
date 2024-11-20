# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np
import seaborn as sns
from singleneuron_plotting_functions import plot_ttlaligned
import os

path = "C:\\Users\\wgo5481\\OneDrive - Northwestern University\\Documents\\pCLAMP - copy\\Data_recordedByDeNard"
# neuron_recordings = os.listdir(path)
resultsfolder_path = "C:\\Users\\wgo5481\\OneDrive - Northwestern University\\Documents\\pCLAMP - copy\\myResults"
resultsfiles_names = os.listdir(resultsfolder_path)
optostim_responses_sthr = [file for file in resultsfiles_names if 'optostimresponses' in file]
optostim_responses_sthr_vclamp = [file for file in optostim_responses_sthr if file.startswith('24')]
neuron_recordings = [name[:7] for name in optostim_responses_sthr_vclamp]

drug_conditions = ['no drug', 'wash in', 'with drug', 'wash out']

# I have looked at all neuron recordings individually and collected response measurements into one table per neuron.
# %% Next goals:
# - plot the baseline response for each neuron
# - see drug effect on response for all neurons in the dataset together

ttlonmeasures_sthr_dfslist = []

for neuron in neuron_recordings:
    # loading in this neuron's data
    neuron_data = SingleNeuron(neuron)
    ttlonmeasures_sthr = pd.read_csv((resultsfolder_path + '\\' + neuron + '_optostimresponses_sthr.csv'), index_col=0)
    # plotting opto response w/o drug:
    neuron_data.plot_ttlaligned(ttlonmeasures_sthr[ttlonmeasures_sthr.drug_condition == 'no drug'],
                                postttl_t_inms=30,
                                prettl_t_inms=5,
                                )
    # collecting the response measures for each neuron
    ttlonmeasures_sthr.loc[:,'neuron_id'] = neuron
    ttlonmeasures_sthr_dfslist.append(ttlonmeasures_sthr)

collected_ttlonmeasures_sthr = pd.concat(ttlonmeasures_sthr_dfslist)
plt.figure()
sns.boxplot(data=collected_ttlonmeasures_sthr, x='neuron_id', y='response_maxamp', hue='drug_condition')

# %% quick-and-dirty comparison to cclamp data
optostim_responses_sthr_cclamp = [file for file in optostim_responses_sthr if not file.startswith('24')]

stim100_dfs = []
stim5_dfs = []

for file in optostim_responses_sthr_cclamp:
    ttlonmeasures_sthr = pd.read_csv((resultsfolder_path + '\\' + file), index_col=0)
    ttlonmeasures_sthr.loc[:, 'neuron_id'] = file[:9]
    ttlonmeasures_sthr_stim100 = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 100].copy()
    ttlonmeasures_sthr_stim5 = ttlonmeasures_sthr[ttlonmeasures_sthr.stim_intensity_pct == 5].copy()
    if len(ttlonmeasures_sthr_stim5) > 0:
        stim5_dfs.append(ttlonmeasures_sthr_stim5)
    if len(ttlonmeasures_sthr_stim100) > 0:
        stim100_dfs.append(ttlonmeasures_sthr_stim100)

collected_ttlonmeasures_sthr_cclamp_stim5 = pd.concat(stim5_dfs)
collected_ttlonmeasures_sthr_cclamp_stim100 = pd.concat(stim100_dfs)
plt.figure()
sns.boxplot(data=collected_ttlonmeasures_sthr_cclamp_stim5, x='neuron_id', y='response_maxamp',
            hue='drug_condition', hue_order=drug_conditions)
plt.figure()
sns.boxplot(data=collected_ttlonmeasures_sthr_cclamp_stim100, x='neuron_id', y='response_maxamp',
            hue='drug_condition', hue_order=drug_conditions)





