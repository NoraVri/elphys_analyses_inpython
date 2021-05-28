# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# finding the relevant neuron recordings
path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

# in principle any IO neuron could have fast-events, but let's first select only the most relevant ones.
# So, let's first narrow down the dataset to neurons where we somehow try to manipulate the fast-events:
# - experiments in Thy1 mice where inputs from all over the brain are activated
# - experiments in RBP mice where inputs from the neocortex are activated
### - experiments where blockers of synaptic inputs are applied
# and let's take only neurons that were recorded for >10min. (since from my notes it seems that
# fast-events can sometimes suddenly be 'turned on' after a few min. of recording, and because
# 10min of recordings seems like a decent start for estimating the overall frequency of events occurring).

# 1. selecting only neuron recordings done on relevant experiment days (evoked synaptic excitation or blocker applied)
# listing the mice with light-evoked excitations experiments
injected_mice = ['HUM042', 'HUM043', 'HUM044', 'HUM045', 'HUM046',
                    'HUM050', 'HUM051', 'HUM052', 'HUM053', 'HUM054', 'HUM055']
genetic_mice = ['Thy1', 'thy1', 'RBP']
# listing mice with blocker-applied experiments
# blockersapplied_mice = experimentdays_metadata.specialchemicals_type.str.contains('AP5')
# blockersapplied_mice[blockersapplied_mice.isna()] = False

# getting a list of all neurons recorded on the days that those mice were used
injected_mice_condition = experimentdays_metadata.virusinjection_ID.isin(injected_mice)
genetic_mice_condition = experimentdays_metadata.genetics.isin(genetic_mice)
lightevokedexcitations_experiments_dates = experimentdays_metadata[
    (injected_mice_condition | genetic_mice_condition)].date
lightevokedexcitations_experimentdays_recordings = recordings_metadata[
    recordings_metadata.date.isin(lightevokedexcitations_experiments_dates)]

relevantneuronrecordings_names = lightevokedexcitations_experimentdays_recordings.name.dropna()
# relevantneuronrecordings_names.dropna()
print(relevantneuronrecordings_names)


# %%
# 2. selecting only neuron recordings where manipulations were actually applied, and that were recorded
# for at least 10min (in case of blockers applied, this requires that the raw data has been annotated appropriately;
# in case of light-evoked excitation we can rely on 'light' appearing in the block name).

evokedexcitations_singleneurons = []
atleast10minrecording_singleneurons = []
atleast30minrecording_singleneurons = []

for neuron in relevantneuronrecordings_names:
    print('importing ' + neuron)
    neuron_data = SingleNeuron(neuron)
    # check time recorded
    rec_time = float(neuron_data.get_timespentrecording()/60)
    if rec_time >= 30:
        atleast30minrecording_singleneurons.append(neuron)
    elif rec_time >= 10:
        atleast10minrecording_singleneurons.append(neuron)
    # check whether light pulses have been applied
    blocknames_list = neuron_data.get_blocknames(printing='off')
    lightactivated_list = [block for block in blocknames_list if 'light' in block]
    if len(lightactivated_list) > 0:
        evokedexcitations_singleneurons.append(neuron)
    # check whether chemicals were actually applied in any of the singleneuron's recordings
    # if neuron_data.rawdata_readingnotes \
    #         and ('chemicalsapplied_blocks' in neuron_data.rawdata_readingnotes.keys()):
    #     blockedexcitations_singleneurons.append(neuron)


print('total no. of neurons in the data set: '
      + str(len(relevantneuronrecordings_names)))
print('no. of neurons that have light-evoked excitations: '
      + str(len(evokedexcitations_singleneurons)))
print('no. of neurons that have at least 10 min. of recording: ' +
      str(len(atleast10minrecording_singleneurons)))
print('no. of neurons that have at least 10 min. of recording AND light-evoked excitations: '
      + str(len(list(set(atleast10minrecording_singleneurons) & set(evokedexcitations_singleneurons)))))
print('no. of neurons that have at least 30 min. of recording: ' +
      str(len(atleast30minrecording_singleneurons)))
print('no. of neurons that have at least 30 min. of recording AND light-evoked excitations: '
      + str(len(list(set(atleast30minrecording_singleneurons) & set(evokedexcitations_singleneurons)))))
# other things to look for (later):
# neurons recorded for > 10 min. and at RT
# select further down also by whether light application was done at different baselinev.


# workflow from here:
# for each neuron, examining depolarizing events (_script_groupingdepolarizingevents):
# - (re-)extracting depolarizing events > 2mV  # in the range below that we find also lots of spikelets and such which are not the focus of this investigation
# - annotating events with appropriate labels (fastevent, other_fast-event, other_event, noiseevent,)
#   manually for each neuron in the dataset
# We will start with the neurons that have >30min. of recording (and at least _some number_ of fast-events),
# and determine from there what are the parameter distributions of each of the groups of events
# (mean and variance in each neuron, and in the population).   # optionally, we can extend the dataset to include neurons recorded on other experiment days (to get more that have long recording times, and to get some that were recorded at RT)
# Parameter distributions will have to be split out by baselinev, and possibly other things - this will be determined
# based on the thorough examination of these lengthy-recording examples.
# Then, we will examine neurons with >10min. of recording and see if they have any events that fall within those parameters.

# The list of neurons with >30min. recording:
# ['20190527A',
# '20190529B',
# '20190529D',
# '20200630C',
# '20200708F',
# '20210110G',
# '20210113H',
# '20210124A',
# '20210426D']