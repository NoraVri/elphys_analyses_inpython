# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# selecting the relevant neuron recordings
path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

evokedexcitations_condition = experimentdays_metadata.genetics.isin(['Thy1'])
conditionsatisfied_dates = experimentdays_metadata[evokedexcitations_condition].date
relevantdates_recordings_metadata = recordings_metadata[recordings_metadata.date.isin(conditionsatisfied_dates)]
relevantdates_recordings_neuronnames = relevantdates_recordings_metadata.name

lightapplied_recordings_neuronnames = []
needs_getting_depolarizingevents_neuronnames = []
for neuron in relevantdates_recordings_neuronnames:
    neuron_data = SingleNeuron(neuron)
    print('imported ' + neuron)
    # check time recorded
    rec_time = float(neuron_data.get_timespentrecording()/60)
    print('total time recorded = ' + str(rec_time) + ' min.')
    # check whether light pulses have been applied
    blocknames_list = neuron_data.get_blocknames(printing='off')
    lightactivated_list = [block for block in blocknames_list if 'light' in block]
    if len(lightactivated_list) > 0:
        lightapplied_recordings_neuronnames.append(neuron)
        print('has light applied')
        if neuron_data.depolarizing_events.empty:
            needs_getting_depolarizingevents_neuronnames.append(neuron)
            print('needs getting depolarizing events')


# %% summary plots for each relevant neuron:
# seeing if there are any neurons with clear amplitude-groups in their light-evoked responses,
# that are comparable to the amplitude-groups of spontaneously occurring fast-events (if there are any).

for neuron in lightapplied_recordings_neuronnames:
    neuron_data = SingleNeuron(neuron)
    print('imported ' + neuron)
    # plotting responses to light, aligned to TTL pulse onset
    blocknames_list = neuron_data.get_blocknames(printing='off')
    lightactivated_list = [block for block in blocknames_list if 'light' in block]


