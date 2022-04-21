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

# getting all IO neuron recordings performed on days that optogenetically activatable inputs were in the slice:
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






# %% making lists:
# - neurons with light-evoked activity;
# - neurons with light-evoked APs;
# - neurons with spont. APs (as extracted depolarizing_events)
# - neurons without depol. events extracted
evokedexcitations_singleneurons = []
evokedAPs_singleneurons = []
spontAPsextracted_singleneurons = []
no_depolevents_yet_singleneurons = []

for neuron in lightevokedneuronrecordings_names:
    print('importing ' + neuron)
    neuron_data = SingleNeuron(neuron)
    # check whether light pulses have been applied
    blocknames_list = neuron_data.get_blocknames(printing='off')
    lightactivated_list = [block for block in blocknames_list if 'light' in block]
    if len(lightactivated_list) > 0:
        evokedexcitations_singleneurons.append(neuron)
        # and if so, whether APs were evoked
        neuron_data.get_ttlonmeasures_fromrawdata()
        if neuron_data.ttlon_measures.response_maxamp.max() > 50:
            evokedAPs_singleneurons.append(neuron)
    # check whether depol.events have been extracted:
    if  (not 'depolarizing_events' in neuron_data.__dir__()) or neuron_data.depolarizing_events.empty:
        no_depolevents_yet_singleneurons.append(neuron)
    # and if so, whether spont.APs were detected:
    else:
        n_spontaps = sum(neuron_data.depolarizing_events[~neuron_data.depolarizing_events.applied_ttlpulse].event_label.str.match('actionpotential').dropna())
        if n_spontaps > 0:
            spontAPsextracted_singleneurons.append(neuron)

# resulting lists:
# evoked APs AND spont.APs extracted (N=32):
# evoked_and_spont_APs = list(set(evokedAPs_singleneurons) & set(spontAPsextracted_singleneurons))
# evoked_and_spont_APs.sort()
evoked_and_spont_APs = ['20190527A',  # our all-time favorite example; spont.AP pre-potentials are 6-10mV, and there are also many fast-events in that range. Light-evoked includes APs with pre-potential and fast-event alone.
                        '20190527C',  # light doesn't evoke APs so much as giant (up to 50mV) fast events; no spont. APs recorded (did see some small fast-events). Not a great recording, and mostly not analyzed yet.
                        '20190529A1', # amplitude grouping not amazingly clear but definitely there, and evoked and spont. look quite identical; very nice example all in all
                        '20190529B',  #*could be an example of evoked APs starting as AIS spikes: pre-potential is always 20mV (and AP very narrow for IO neuron). No spont. APs or fastevents recorded.
                        '20190529D',  # low freq spont events and APs; spont.APs come from an 8mV fast-event, evoked ones from a 20mV one
                        '20200630B2',
                        '20200630C',  # response to light always seems to have fast component (and often leads to AP); does have spont.fastevents (in amplitude groups) but spont.APs don't have a clear pre-potential (though it's probably there)
                        '20200630D',
                        '20200701A',  # of 4 spont.APs 3 have the same pre-potential amplitude (grouping very clear); *needs more analysis to find fast-events
                        '20200706E',  # most APs seem to have compound pre-potential; *needs more analysis to find fast-events
                        '20200707E',
                        '20200708B',  # just two spont.APs, one clearly from pre-potential; *needs more analysis to find fastevents
                        '20200708C',  # just one spont.AP, not from pre-potential (high baselinev)
                        '20200708D',  # all spont.APs start from largest-amp fast-event except for one (which starts from a smaller-amp one); lots of spont.fastevents (amplitude grouping not very clear). Evoked is practically always AP, with decreased light fast-event that goes away with hyperpolarization but lots of compoundness going on.
                        '20200708F',  # not a very nice example, lots of compoundness going on
                        '20201125B',  # loads of spont.APs, but looks like badly deteriorating recoring; *needs more analysis to find fastevents
                        '20201125C',  # just one spont.AP, not from pre-potential (high baselinev)
                        '20201125D',  #*has some spont.APs from pre-potential, largest fast-event matches amplitude; very clear difference with APs evoked from synaptic potential
                        '20210105B',  # just one spont.AP, possibly from pre-potential; *needs more analysis for fast-events
                        '20210105D',  # terrible baselinev for the two spont.APs (>-20)
                        '20210110A',  #*APs all seem to start from compound pre-potential; *needs more analysis
                        '20210110D',  # only two spont.APs, one clearly from pre-potential; *needs more analysis
                        '20210110E',  # four spont.APs none from pre-potential (baselinev ~-24mV)
                        '20210110F',
                        '20210113D',  # spont.APs seem to have mostly compound pre-potentials; *needs more analysis
                        '20210113G',  # possibly all spont.APs from pre-potential; looks like a badly deteriorating recording though; has spont.events to match
                        '20210113H',  # practically all spont.APs from the largest-amp fastevent (~10mV)
                        '20210123B',  # bad baselinev, total mess
                        '20210124B', '20210124C', '20210124D',
                        '20210413B',  # noisy recording with bad baselinev
                        '20210426B'   # most APs from pre-potential, no spont.fast events (pretty bad Vrest throughout recording)
                        ]

# %% plots
for neuron in evoked_and_spont_APs:
    singleneuron_data = SingleNeuron(neuron)

    des_df = singleneuron_data.depolarizing_events
    spont_events = ~des_df.applied_ttlpulse
    aps = des_df.event_label == 'actionpotential'
    spont_aps = (aps & spont_events)
    fastevents = des_df.event_label == 'fastevent'
    spont_fastevents = (fastevents & spont_events)

    # singleneuron_data.plot_rawdatatraces_ttlaligned()
    if sum(spont_aps) > 0:
        singleneuron_data.plot_depolevents(spont_aps, colorby_measure='baselinev')
    if sum(spont_fastevents) > 0:
        singleneuron_data.plot_depolevents(spont_fastevents, colorby_measure='baselinev')
