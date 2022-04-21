# %% imports
import os

from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# metadata imports
path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

MDJ_mice = ['HUM050', 'HUM051', 'HUM052', 'HUM053', 'HUM054', 'HUM055']
MDJ_mice_condition = experimentdays_metadata.virusinjection_ID.isin(MDJ_mice)
MDJ_mice_experiments_dates = experimentdays_metadata[MDJ_mice_condition].date
MDJ_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(MDJ_mice_experiments_dates)]
MDJ_mice_neuronrecordings_names = MDJ_mice_neuronrecordings.name.dropna()

midbrain_mice = ['HUM042', 'HUM043', 'HUM044', 'HUM045', 'HUM046',]
midbrain_mice_experiments_dates = experimentdays_metadata[experimentdays_metadata.virusinjection_ID.isin(midbrain_mice)].date
midbrain_mice_recordings_names = recordings_metadata[recordings_metadata.date.isin(midbrain_mice_experiments_dates)].name.dropna()

Thy1_mice = ['Thy1', 'thy1']
Thy1_mice_condition = experimentdays_metadata.genetics.isin(Thy1_mice)
Thy1_mice_experiments_dates = experimentdays_metadata[Thy1_mice_condition].date
Thy1_mice_neuronrecordings = recordings_metadata[recordings_metadata.date.isin(Thy1_mice_experiments_dates)]
Thy1_mice_neuronrecordings_names = Thy1_mice_neuronrecordings.name.dropna()

RBP_mice = ['RBP', 'RBP4-cre/Ai32']
RBP_mice_experiments_dates = experimentdays_metadata[experimentdays_metadata.genetics.isin(RBP_mice)].date
RBP_mice_recordings_names = recordings_metadata[recordings_metadata.date.isin(RBP_mice_experiments_dates)].name.dropna()


allneuronrecordings_serieslist = [MDJ_mice_neuronrecordings_names,
                                  midbrain_mice_recordings_names,
                                  Thy1_mice_neuronrecordings_names,
                                  RBP_mice_recordings_names]
lightevokeddays_neuronrecordings_names = pd.concat(allneuronrecordings_serieslist)

# I don't have any experiments in mice with optogenetically-labeled things where TTl-on is used for anything besides
# activating the light. So, we can use get_ttlonmeasures to identify neurons that actually had light responses recorded.
# lightevokedneurons_list = []
# lightevokedAPsneurons_list = []
# for neuron in lightevokeddays_neuronrecordings_names:
#     neuron_data = SingleNeuron(neuron)
#     neuron_data.get_ttlonmeasures_fromrawdata()
#     if not neuron_data.ttlon_measures.empty:
#         lightevokedneurons_list.append(neuron)
#         if neuron_data.ttlon_measures.response_maxamp.max() > 40:
#             lightevokedAPsneurons_list.append(neuron)

# print(lightevokedneurons_list)
lightevokedneurons_list = ['20210411A', '20210411B', '20210411C', '20210411F', '20210413A', '20210413B', '20210426B', '20210426C', '20210426D', '20210426E', '20210426F', '20210110A', '20210110C', '20210110D', '20210110E', '20210110F', '20210110G', '20210113A', '20210113B', '20210113C', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210123C', '20210123D', '20210124A', '20210124B', '20210124C', '20210124D', '20210203A', '20210203B', '20210203C', '20190527A', '20190527C', '20190529A1', '20190529B', '20190529C', '20190529D', '20190529E', '20200630A', '20200630B1', '20200630B2', '20200630C', '20200630D', '20200701A', '20200701B', '20200701D', '20200706B', '20200706D', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20200708G', '20210105A', '20210105B', '20210105C', '20210105D', '20210105E', '20210429A1', '20210429A2', '20210429B', '20200818B', '20200818C', '20201124A', '20201124C', '20201125B', '20201125C', '20201125D', '20201125E', '20201125F']
  # removed cell20200707B, since it's not an IO neuron
# print(lightevokedAPsneurons_list)
lightevokedAPsneurons_list = ['20210413B', '20210426B', '20210110A', '20210110D', '20210110E', '20210110F', '20210113D', '20210113F', '20210113G', '20210113H', '20210123B', '20210124B', '20210124C', '20210124D', '20190527A', '20190527C', '20190529A1', '20190529B', '20190529D', '20200630A', '20200630B2', '20200630C', '20200630D', '20200701A', '20200706E', '20200707E', '20200708B', '20200708C', '20200708D', '20200708F', '20210105B', '20210105D', '20201124C', '20201125B', '20201125C', '20201125D']


# %% finding neurons with both spontaneous and light-evoked APs/fast-events
# also: extracting spontaneous events for neurons that didn't get that done yet
# rawdatacleanup_required_list = []
# depolevents_notextracted_list = []
has_evokedAPsextracted_list = []
has_spontAPsextracted_list = []

storedresultsfolder_path = path + '\\' + 'myResults'
resultsfiles_list = os.listdir(storedresultsfolder_path)
for neuron in lightevokedneurons_list:
    neuron_resultsfiles = [file for file in resultsfiles_list if neuron in file]
    # if not neuron_resultsfiles:
    #     rawdatacleanup_required_list.append(neuron)
    # else:
    neuron_depoleventsfile = [file for file in neuron_resultsfiles if 'depolarizing_events' in file]
    if not neuron_depoleventsfile:
        neuron_data = SingleNeuron(neuron)
        neuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2, ttleffect_window=15)
        neuron_data.write_results()
        neuron_depolevents = neuron_data.depolarizing_events
        spontaps = ((neuron_depolevents.event_label == 'actionpotential') & ~(neuron_depolevents.applied_ttlpulse))
        evokedaps = ((neuron_depolevents.event_label == 'actionpotential') & (neuron_depolevents.applied_ttlpulse))
    else:
        neuron_depoleventsfile_path = storedresultsfolder_path + '\\' + neuron_depoleventsfile[0]
        neuron_depolevents = pd.read_csv(neuron_depoleventsfile_path, index_col=0)
        spontaps = ((neuron_depolevents.event_label == 'actionpotential') & ~(neuron_depolevents.applied_ttlpulse))
        evokedaps = ((neuron_depolevents.event_label == 'actionpotential') & (neuron_depolevents.applied_ttlpulse))
    if sum(spontaps) > 0:
        has_spontAPsextracted_list.append(neuron)
    if sum(evokedaps) > 0:
        has_evokedAPsextracted_list.append(neuron)

# print(rawdatacleanup_required_list)
# ['20200701B', no cleanups to apply
# '20200707B', not an IO neuron
# '20200707E', no cleanups to apply
# '20210113D', no cleanups to apply
# '20210426C', no cleanups to apply
# '20210429B'  no cleanups to apply
# ]

spontandevokedaps_neurons_list = list(set(has_spontAPsextracted_list) & set(has_evokedAPsextracted_list))
# print(spontandevokedaps_neurons_list)
# ['20190527A', '20190529A1', '20190529D', '20200630C', '20200708D', '20200708F', '20201125D', '20210105D', '20210113G', '20210113H', '20210413B', '20210426B']
# none are from MDJ-labeled experiments (some are from midbrain-labeled experiments)

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


# %% split out by where the optogenetically activated innervation is coming from
# %%
Thy1_spontandevokedAPs_neurons = list(set(spontandevokedaps_neurons_list) & set(Thy1_mice_neuronrecordings_names))
for neuron in Thy1_spontandevokedAPs_neurons:
    neuron_data = SingleNeuron(neuron)
    spontaps = ((neuron_data.depolarizing_events.event_label == 'actionpotential')
                & ~(neuron_data.depolarizing_events.applied_ttlpulse))
    neuron_data.plot_depolevents(spontaps,
                                 colorby_measure='baselinev',
                                 plotwindow_inms=30,
                                 plt_title=' spont APs')
    spontfastevents = (neuron_data.depolarizing_events.event_label == 'fastevent')
    if sum(spontfastevents) > 1:
        neuron_data.plot_depolevents(spontfastevents,
                                     colorby_measure='baselinev',
                                     plotwindow_inms=30,
                                     plt_title=' spont fastevents'
                                     )
    else:
        possibly_spontfastevents = (neuron_data.depolarizing_events.amplitude > 3)
        if sum(possibly_spontfastevents) > 1:
            neuron_data.plot_depolevents(possibly_spontfastevents,
                                         colorby_measure='baselinev',
                                         plotwindow_inms=30,
                                         plt_title=' spont large-amp events'
                                         )
    neuron_data.plot_rawdatatraces_ttlaligned(plt_title='evoked responses')
# recordings of particular interest:


# %%
RBP_spontandevokedAPs_neurons = list(set(spontandevokedaps_neurons_list) & set(RBP_mice_recordings_names))
for neuron in RBP_spontandevokedAPs_neurons:
    neuron_data = SingleNeuron(neuron)
    spontaps = ((neuron_data.depolarizing_events.event_label == 'actionpotential')
                & ~(neuron_data.depolarizing_events.applied_ttlpulse))
    neuron_data.plot_depolevents(spontaps,
                                 colorby_measure='baselinev',
                                 plotwindow_inms=30,
                                 plt_title=' spont APs')
    spontfastevents = (neuron_data.depolarizing_events.event_label == 'fastevent')
    if sum(spontfastevents) > 1:
        neuron_data.plot_depolevents(spontfastevents,
                                     colorby_measure='baselinev',
                                     plotwindow_inms=30,
                                     plt_title=' spont fastevents'
                                     )
    else:
        possibly_spontfastevents = (neuron_data.depolarizing_events.amplitude > 3)
        if sum(possibly_spontfastevents) > 1:
            neuron_data.plot_depolevents(possibly_spontfastevents,
                                         colorby_measure='baselinev',
                                         plotwindow_inms=30,
                                         plt_title=' spont large-amp events'
                                         )
    neuron_data.plot_rawdatatraces_ttlaligned(plt_title='evoked responses')
# recordings of particular interest:

# %%
# MDJ_spontandevokedAPs_neurons = list(set(spontandevokedaps_neurons_list) & set(MDJ_mice_neuronrecordings_names))
# for neuron in MDJ_spontandevokedAPs_neurons:
#     neuron_data = SingleNeuron(neuron)
#     spontaps = ((neuron_data.depolarizing_events.event_label == 'actionpotential')
#                 & ~(neuron_data.depolarizing_events.applied_ttlpulse))
#     neuron_data.plot_depolevents(spontaps,
#                                  colorby_measure='baselinev',
#                                  plotwindow_inms=30,
#                                  plt_title=' spont APs')
#     spontfastevents = (neuron_data.depolarizing_events.event_label == 'fastevent')
#     if sum(spontfastevents) > 1:
#         neuron_data.plot_depolevents(spontfastevents,
#                                      colorby_measure='baselinev',
#                                      plotwindow_inms=30,
#                                      plt_title=' spont fastevents'
#                                      )
#     else:
#         possibly_spontfastevents = (neuron_data.depolarizing_events.amplitude > 3)
#         if sum(possibly_spontfastevents) > 1:
#             neuron_data.plot_depolevents(possibly_spontfastevents,
#                                          colorby_measure='baselinev',
#                                          plotwindow_inms=30,
#                                          plt_title=' spont large-amp events'
#                                          )
#     neuron_data.plot_rawdatatraces_ttlaligned(plt_title='evoked responses')

MDJ_lightactivated_neurons = list(set(lightevokedneurons_list) & set(MDJ_mice_neuronrecordings_names))
MDJ_lightactivated_neurons.sort()
for neuron in MDJ_lightactivated_neurons:
    neuron_data = SingleNeuron(neuron)
    neuron_data.plot_rawdatatraces_ttlaligned(plt_title='evoked responses')
    spontaps = ((neuron_data.depolarizing_events.event_label == 'actionpotential')
                & ~(neuron_data.depolarizing_events.applied_ttlpulse))
    if sum(spontaps) > 0:
        neuron_data.plot_depolevents(spontaps,
                                     colorby_measure='baselinev',
                                     plotwindow_inms=30,
                                     plt_title=' spont APs')
    spontfastevents = (neuron_data.depolarizing_events.event_label == 'fastevent')
    if sum(spontfastevents) > 0:
        neuron_data.plot_depolevents(spontfastevents,
                                     colorby_measure='baselinev',
                                     plotwindow_inms=30,
                                     plt_title=' spont fastevents')
    else:
        largeamp_spontevents = ((neuron_data.depolarizing_events.event_label.isna())
                                & ~(neuron_data.depolarizing_events.applied_ttlpulse)
                                & (neuron_data.depolarizing_events.amplitude > 3))
        if sum(largeamp_spontevents) > 0:
            neuron_data.plot_depolevents(largeamp_spontevents,
                                         colorby_measure='baselinev',
                                         plotwindow_inms=30,
                                         plt_title=' large amp spont events')

# recordings of particular interest:
#20210411F - clear example of evoked fast-events: multiple amp groups, largest ones disappear first with hyperpolarization. Too bad it has terrible baselinev (>-30mV even with huge -DC) and no spont.APs.
#20210413B - oscillating throughout with spont.fast-events, responding to light with APs or fast-things at hyperpolarized potentials
#20210426B - has spont.APs and fast-events, light evokes AP almost every time. Bad baselinev and noisy data.

# %%
midbrain_spontandevokedAPs_neurons = list(set(spontandevokedaps_neurons_list) & set(midbrain_mice_recordings_names))
for neuron in midbrain_spontandevokedAPs_neurons:
    neuron_data = SingleNeuron(neuron)
    spontaps = ((neuron_data.depolarizing_events.event_label == 'actionpotential')
                & ~(neuron_data.depolarizing_events.applied_ttlpulse))
    neuron_data.plot_depolevents(spontaps,
                                 colorby_measure='baselinev',
                                 plotwindow_inms=30,
                                 plt_title=' spont APs')
    spontfastevents = (neuron_data.depolarizing_events.event_label == 'fastevent')
    if sum(spontfastevents) > 1:
        neuron_data.plot_depolevents(spontfastevents,
                                     colorby_measure='baselinev',
                                     plotwindow_inms=30,
                                     plt_title=' spont fastevents'
                                     )
    else:
        possibly_spontfastevents = (neuron_data.depolarizing_events.amplitude > 3)
        if sum(possibly_spontfastevents) > 1:
            neuron_data.plot_depolevents(possibly_spontfastevents,
                                         colorby_measure='baselinev',
                                         plotwindow_inms=30,
                                         plt_title=' spont large-amp events'
                                         )
    neuron_data.plot_rawdatatraces_ttlaligned(plt_title='evoked responses')
# recordings of particular interest:
# 210113H

