# %% imports
from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

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
# Total number of neurons in the dataset: N = 78.












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
        if sum(~(neuron_data.depolarizing_events.event_label.isna())) > 0:
            labeled_fastevents = neuron_data.depolarizing_events.event_label == 'fastevent'
            if sum(labeled_fastevents) > 0:
                has_labeled_fastevents_list.append(neuron)
            aps = neuron_data.depolarizing_events.event_label.str.contains('actionpotential').dropna()  # getting both spont.APs and ones on_currentpulsechange
            if sum(aps) > 0:
                has_APs_list.append(neuron)
# %% neuron recordings lists
# list of all neuron recordings in the dataset:
dataset_neuronrecordings_list = [
    '20190527A',  # checked APs; checked fastevents; checked neatevents
    '20190527B',  # checked APs; checked fastevents; checked neatevents
    '20190527C',  # no APs (!); checked fastevents; no neatevents  - !light may be evoking highly degenerate APs; APs cannot be evoked through DC
    '20190529A1', # checked APs; checked fastevents; checked neatevents
    '20190529A2', # checked APs; checked fastevents; no neatevents
    '20190529B',  # checked APs; no fastevents; checked neatevents
    '20190529C',  # no APs; checked fastevents; no neatevents
    '20190529D',  # checked APs; checked fastevents; no neatevents
    '20190529E',  # checked APs; no fastevents; no neatevents
    '20200630A',  # checked APs; no fastevents; no neatevents
    '20200630B1', # checked APs; no fastevents; no neatevents
    '20200630B2', # checked APs; no fastevents
    '20200630C',  # checked APs; checked fastevents; checked neatevents
    '20200630D',  # checked APs; checked fastevents; checked neatevents (!)  - !about half of fastevents have an AHP that looks like it comes from the network - not sure if averaging is fair, even though they do all look 'neat'
    '20200701A',  #
    '20200701B',  #
    '20200701D',  # no APs; no fastevents; no neatevents
    '20200706A',
    '20200706B',  #
    '20200706D',  #
    '20200706E',  #
    '20200707E',  #
    '20200708A',
    '20200708B',  #
    '20200708C',  #
    '20200708D',  # checked APs; checked fastevents; checked neatevents
    '20200708E',
    '20200708F',  # checked APs; checked fastevents; checked neatevents
    '20200708G',  #
    '20200818B',  # checked APs; checked fastevents; checked neatevents (APs only current-evoked)
    '20200818C',  #
    '20201124C',  #
    '20201125B',  #
    '20201125C',  #
    '20201125D',  # checked APs; checked fastevents; checked neatevents
    '20201125E',  #
    '20201125F',  #
    '20210105A',  #
    '20210105B',
    '20210105C',  #
    '20210105D',
    '20210105E',  #
    '20210110A',
    '20210110B',
    '20210110C',  #
    '20210110D',  #
    '20210110E',  #
    '20210110F',  #
    '20210110G',  # checked APs; checked fastevents; checked neatevents (only three spont.subthreshold events; APs only current-evoked)
    '20210113A',
    '20210113B',  #
    '20210113C',  #
    '20210113D',  #
    '20210113E',
    '20210113F',  #
    '20210113G',  # checked APs; checked fastevents; checked neatevents
    '20210113H',  # checked APs; checked fastevents; checked neatevents (very nice example for evoking 2 different amplitude fastevents (and an AP from the largest one))
    '20210123B',  #
    '20210123D',  #
    '20210124A',  # checked APs; checked fastevents; checked neatevents
    '20210124B',  # checked APs; checked fastevents; checked neatevents
    '20210124C',
    '20210124D',
    '20210203A',  #
    '20210203B',  #
    '20210203C',
    '20210407C',
    '20210411A',  #
    '20210411B',  #
    '20210411C',  #
    '20210411F',  # no APs; checked fastevents; no neatevents
    '20210413A',  #
    '20210413B',  # checked APs; checked fastevents; no neatevents
    '20210426B',  #
    '20210426C',  #
    '20210426D',  # checked APs; checked fastevents; checked neatevents (spont.APs are very weirdly degenerate, as though no Na-component [while fastevents persist...])
    '20210426E',  #
    '20210429B'   #
]

# sub-lists:
has_labeled_fastevents_list = ['20190527A', '20190529A1', '20190529C', '20190529D', '20200630C', '20200708D', '20200708F', '20200818B', '20201125D', '20210110G', '20210113G', '20210113H', '20210124A', '20210124B', '20210411F', '20210413B', '20210426D']
has_APs_list = ['20190527A', '20190529A1', '20190529B', '20190529D', '20200630C', '20200708D', '20200708F', '20200818B', '20210110G', '20210113G', '20210113H', '20210124A', '20210124B', '20210413B', '20210426D']
has_lightactivations_list = ['20190527A', '20190527C', '20190529A1', '20190529B', '20190529C', '20190529D', '20190529E', '20200630A', '20200630B1', '20200630B2', '20200630C', '20200630D', '20200701A', '20200701B', '20200701D', '20200706B', '20200706D', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20200708G', '20200818B', '20200818C', '20201124C', '20201125B', '20201125C', '20201125D', '20201125E', '20201125F', '20210105A', '20210105B', '20210105C', '20210105D', '20210105E', '20210110A', '20210110C', '20210110D', '20210110E', '20210110F', '20210110G', '20210113A', '20210113B', '20210113C', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210123D', '20210124A', '20210124B', '20210124C', '20210124D', '20210203A', '20210203B', '20210203C', '20210411A', '20210411B', '20210411F', '20210413A', '20210413B', '20210426B', '20210426C', '20210426D', '20210426E', '20210429B']
has_lightevokedAPs_list = ['20190527A', '20190527C', '20190529A1', '20190529B', '20190529D', '20200630A', '20200630B2', '20200630C', '20200630D', '20200701A', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20201124C', '20201125B', '20201125C', '20201125D', '20210105B', '20210105D', '20210110A', '20210110D', '20210110E', '20210110F', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210124B', '20210124C', '20210124D', '20210413B', '20210426B']







# %% one figure for all neurons with neat fast-events: neat fast-events normalized and averaged
from singleneuron_analyses_functions import get_events_average
figure1, axes1 = plt.subplots(1, 2)
figure2, axes2 = plt.subplots(1, 2)
neuron_list = has_labeled_fastevents_list
colormap = mpl.cm.Paired
cmnormalizer = mpl.colors.Normalize(0, len(neuron_list))
for i, neuron in enumerate(neuron_list):
    neuron_data = SingleNeuron(neuron)
    neuron_depolarizingevents = neuron_data.depolarizing_events
    if 'neat_event' in neuron_data.depolarizing_events.keys():
        neat_fastevents = ((neuron_depolarizingevents.event_label == 'fastevent') & (neuron_depolarizingevents.neat_event))
        n_events = sum(neat_fastevents)
        normalized_neatfastevents_avg, \
        normalized_neatfastevents_std, \
        time_axis = get_events_average(neuron_data.blocks,
                                       neuron_data.depolarizing_events,
                                       neuron_data.rawdata_readingnotes['getdepolarizingevents_settings'],
                                       neat_fastevents,
                                       timealignto_measure='rt20_start_idx',
                                       prealignpoint_window_inms=3,
                                       plotwindow_inms=20,
                                       do_normalizing=True)
        linecolor = colormap(cmnormalizer(i))
        axes1[0].plot(time_axis, normalized_neatfastevents_avg, linewidth=2.5, color=linecolor)
        axes1[0].plot(time_axis, (normalized_neatfastevents_avg - normalized_neatfastevents_std), '--', color=linecolor)
        axes1[0].plot(time_axis, (normalized_neatfastevents_avg + normalized_neatfastevents_std), '--', color=linecolor)
        axes1[0].set_xlabel('time (ms)')
        diff_events_avg = np.diff(normalized_neatfastevents_avg)
        axes1[1].plot(normalized_neatfastevents_avg[:-1:], diff_events_avg, color=linecolor, label=(neuron_data.name + ' N=' + str(n_events) + ' events'))
    # figure2: fastevents within baselinerange
        lower_lim = -55
        upper_lim = -45
        baselinerange_neat_fastevents = (neat_fastevents
                                         & (neuron_depolarizingevents.baselinev > lower_lim)
                                         & (neuron_depolarizingevents.baselinev < upper_lim))
        n_baselinerange_events = sum(baselinerange_neat_fastevents)
        if n_baselinerange_events > 0:
            normalized_neatfastevents_avg, \
            normalized_neatfastevents_std, \
            time_axis = get_events_average(neuron_data.blocks,
                                           neuron_data.depolarizing_events,
                                           neuron_data.rawdata_readingnotes['getdepolarizingevents_settings'],
                                           baselinerange_neat_fastevents,
                                           timealignto_measure='rt20_start_idx',
                                           prealignpoint_window_inms=3,
                                           plotwindow_inms=20,
                                           do_normalizing=True)
            linecolor = colormap(cmnormalizer(i))
            axes2[0].plot(time_axis, normalized_neatfastevents_avg, linewidth=2.5, color=linecolor)
            axes2[0].plot(time_axis, (normalized_neatfastevents_avg - normalized_neatfastevents_std), '--',
                          color=linecolor)
            axes2[0].plot(time_axis, (normalized_neatfastevents_avg + normalized_neatfastevents_std), '--',
                          color=linecolor)
            axes2[0].set_xlabel('time (ms)')
            diff_events_avg = np.diff(normalized_neatfastevents_avg)
            axes2[1].plot(normalized_neatfastevents_avg[:-1:], diff_events_avg, color=linecolor,
                          label=(neuron_data.name + ' N=' + str(n_baselinerange_events) + ' events'))

    axes1[1].set_xlabel('V')
    axes1[1].set_ylabel('dV/dt')
    axes1[1].legend(loc='upper left')
    axes2[1].set_xlabel('V')
    axes2[1].set_ylabel('dV/dt')
    axes2[1].legend(loc='upper left')


# %% plotting APs for neurons that have them extracted
neuron_list = has_APs_list
for neuron in neuron_list:
    neuron_data = SingleNeuron(neuron)
    neuron_data.get_ttlonmeasures_fromrawdata()
    neuron_data.plot_rawdatatraces_ttlaligned(*neuron_data.ttlon_measures.file_origin.unique())
    spont_aps = (neuron_data.depolarizing_events.event_label == 'actionpotential') & (~neuron_data.depolarizing_events.applied_ttlpulse)
    neuron_data.plot_depolevents(spont_aps,
                                 colorby_measure='baselinev',
                                 prealignpoint_window_inms=10,
                                 plt_title=' spont.APs')
    currentevoked_aps = (neuron_data.depolarizing_events.event_label == 'actionpotential_on_currentpulsechange')
    if sum(currentevoked_aps) > 0:
        neuron_data.plot_depolevents(currentevoked_aps,
                                     colorby_measure='baselinev',
                                     plt_title=' DC-evoked APs')

# %%
# interesting neurons:
# 190527A,
# 190529A1 - twin to 190527A
# 190529B - has a fastevent of 20mV amplitude?
# 190529D - fastevent (20mV) = AIS spike?
# 200630B2 - very nice resemblance between spont. and light-evoked APs
# 200630D - gets hyperpolarized quite far, still firing APs (also spont); no DC-evoked APs
# 200701A - twin to 200630D
# 200708D - light activations get smaller amp with hyperpolarization, until fastevent disappears
# 201125C - example of neuron without any fastevents?
# 201125D - our favorite example of light-activated synapse and spont.fastevent
# 210110F - just looks nice
# 210113D - spont.APs at baselinev=-60mV without shoulder
# 210113H - two different amp fastevents activated by light (riding very small synapse)
# 210124B - fastevent+degenerate AIS spike?














