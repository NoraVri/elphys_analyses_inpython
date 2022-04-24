# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# In this script: analysis of APs as triggered from fast-events.
# Dataset: neurons recorded on days with optogenetic activation of inputs to IO.

# metadata imports
path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

# getting all IO neuron recordings performed on days that optogenetically activatable inputs were in the slice,
# split out per type of labeled inputs:
MDJ_mice = ['HUM042', 'HUM043', 'HUM044', 'HUM045', 'HUM046',
                    'HUM050', 'HUM051', 'HUM052', 'HUM053', 'HUM054', 'HUM055']
RBP_mice = ['RBP', 'RBP4-cre/Ai32']
Thy1_mice = ['Thy1', 'thy1']

injected_mice_condition = experimentdays_metadata.virusinjection_ID.isin(MDJ_mice)
RBP_mice_condition = experimentdays_metadata.genetics.isin(RBP_mice)
Thy1_mice_condition = experimentdays_metadata.genetics.isin(Thy1_mice)

lightevokedexcitations_experiments_dates = experimentdays_metadata[
    (injected_mice_condition | RBP_mice_condition | Thy1_mice_condition)].date
lightevokedexcitations_experimentdays_IOneuronrecordings = recordings_metadata[
    recordings_metadata.date.isin(lightevokedexcitations_experiments_dates)
    & (recordings_metadata.anatomical_location == 'inferior_olive')
    ]
# IOneurons_recorded_onLightActivatedDays = lightevokedexcitations_experimentdays_IOneuronrecordings.name.dropna()

# analyses step0: go to script_rawdata_importing and go over raw data for each neuron in the dataset (N=99).
# analyses step0.1: get list of neurons again, but without those whose total_t_recorded_in_s = 0 (neuron data excluded)
IOneurons_recorded_onLightActivatedDays = lightevokedexcitations_experimentdays_IOneuronrecordings[
    (lightevokedexcitations_experimentdays_IOneuronrecordings.total_t_recorded_in_s > 0)].name.dropna()
# Total number of neurons in the dataset: N = 77.

# %% analyses step1: getting APs and depolarizing events for all neurons in the dataset.
# analyses step1.1: determining which neurons have spont. fastevents and/or APs, and light-evoked events and/or APs.
# Some neurons have been of particular interest before and have had depolarizing events extracted and labeled, (or are in the process of getting that done - will have to check up on that)
# but most neurons in this dataset have not yet been run through depolarizingevents-extraction.
has_labeled_fastevents_list = []
has_APs_list = []
hasno_depolevents_extracted_list = []
# I don't have any experiments in mice with optogenetically-labeled things where TTl-on is used for anything besides
# activating the light. So, we can use get_ttlonmeasures to identify neurons that actually had light responses recorded.
has_lightactivations_list = []
has_lightevokedAPs_list = []
# filling in the lists:
for neuron in IOneurons_recorded_onLightActivatedDays:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    if not neuron_data.ttlon_measures.empty:
        has_lightactivations_list.append(neuron)
        if neuron_data.ttlon_measures.response_maxamp.max() > 40:
            has_lightevokedAPs_list.append(neuron)
    if neuron_data.depolarizing_events.empty:
        hasno_depolevents_extracted_list.append(neuron)
    else:
        labeled_fastevents = neuron_data.depolarizing_events.event_label == 'fastevent'
        if sum(labeled_fastevents) > 0:
            has_labeled_fastevents_list.append(neuron)
        aps = neuron_data.depolarizing_events.event_label.str.contains('actionpotential').dropna()  # getting both spont.APs and ones on_currentpulsechange
        if sum(aps) > 0:
            has_APs_list.append(neuron)
# %%
# resulting lists:
has_labeled_fastevents_list = ['20190527A', # checked fastevents and neatevents
                               '20190529A1', # checked fastevents and neatevents
                               '20190529C',
                               '20190529D', '20200630C', '20200708D', '20200708F', '20200818B', '20210110G', '20210113G', '20210113H', '20210124A', '20210426D']
has_APs_list = ['20190527A', # checked APs
                # '20190527C',
                '20190529A1', # checked APs
                '20190529B',  # checked APs - light-evoked only (checked fastevents also (there are none); no spont APs, not even with +DC)
                '20190529D', '20200630B2', '20200630C', '20200630D', '20200701A', '20200706B', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20200818B', '20200818C', '20201124C', '20201125B', '20201125C', '20201125E', '20201125F', '20210105A', '20210105C', '20210105E', '20210110C', '20210110D', '20210110E', '20210110F', '20210110G', '20210113B', '20210113C', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210123D', '20210124A', '20210124B', '20210203A', '20210203B', '20210411A', '20210411B', '20210411C', '20210413A', '20210413B', '20210426C', '20210426D', '20210426E']
hasno_depolevents_extracted_list = ['20190527B', '20190529A2', '20190529E', '20200630A', '20200630B1', '20200706A', '20200708A', '20200708E', '20201125D', '20210105B', '20210105D', '20210110A', '20210110B', '20210113A', '20210113E', '20210124C', '20210124D', '20210203C', '20210407C', '20210426B']
has_lightactivations_list = ['20190527A', '20190527C', '20190529A1', '20190529B', '20190529C', '20190529D', '20190529E', '20200630A', '20200630B1', '20200630B2', '20200630C', '20200630D', '20200701A', '20200701B', '20200706B', '20200706D', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20200708G', '20200818B', '20200818C', '20201124C', '20201125B', '20201125C', '20201125D', '20201125E', '20201125F', '20210105A', '20210105B', '20210105C', '20210105D', '20210105E', '20210110A', '20210110C', '20210110D', '20210110E', '20210110F', '20210110G', '20210113A', '20210113B', '20210113C', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210123D', '20210124A', '20210124B', '20210124C', '20210124D', '20210203A', '20210203B', '20210203C', '20210411A', '20210411B', '20210411F', '20210413A', '20210413B', '20210426B', '20210426C', '20210426D', '20210426E', '20210429B']
has_lightevokedAPs_list = ['20190527A', '20190527C', '20190529A1', '20190529B', '20190529D', '20200630A', '20200630B2', '20200630C', '20200630D', '20200701A', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20201124C', '20201125B', '20201125C', '20201125D', '20210105B', '20210105D', '20210110A', '20210110D', '20210110E', '20210110F', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210124B', '20210124C', '20210124D', '20210413B', '20210426B']



















