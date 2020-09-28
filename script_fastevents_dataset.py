# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# %% finding the relevant neuron recordings
path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

# in principle any IO neuron could have fast-events, but let's first select only the most relevant ones.
# So, let's first narrow down the dataset to neurons where we somehow try to manipulate the fast-events:
# - experiments in Thy1 mice where inputs from all over the brain are activated
# - experiments in RBP mice where inputs from the neocortex are activated
# - experiments where blockers of synaptic inputs are applied
# and let's take only neurons that were recorded for >10min. (since from my notes it seems that
# fast-events can sometimes suddenly be 'turned on' after a few min. of recording, and because
# 10min of recordings seems like a decent start for estimating the overall frequency of events occurring).

# 1. selecting only neuron recordings done on relevant experiment days (evoked synaptic excitation or blocker applied)
evokedexcitations_condition = experimentdays_metadata.genetics.isin(['Thy1', 'RBP'])
blockedexcitations_condition = experimentdays_metadata.specialchemicals_type.str.contains('AP5')
blockedexcitations_condition[blockedexcitations_condition.isna()] = False

manipulatedexcitations_experiments_dates = \
    experimentdays_metadata[
        evokedexcitations_condition | blockedexcitations_condition
                            ].date

manipulatedexcitations_experiments_recordings = \
    recordings_metadata[recordings_metadata.date.isin(manipulatedexcitations_experiments_dates)]

manipulatedexcitations_singleneurons_names = manipulatedexcitations_experiments_recordings.name

# 2. selecting only neuron recordings where manipulations were actually applied, and were recorded for at least 10min
#(in case of blockers applied, this requires that the raw data has been annotated appropriately;
# in case of light-evoked excitation we can rely on 'light' appearing in the block name).
