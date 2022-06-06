# %% imports
import os

from singleneuron_class import SingleNeuron
import matplotlib as mpl
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

# %% getting depolarizing events for neurons recorded on days with QX
neurons = ['20220524A', # no spont.APs, evoked APs, not sure about fastevents (two events with amp just >3mV)
           '20220524B', # no spont.APs, evoked APs, no fastevents
           '20220524C', # no spont.APs, evoked APs, fastevents
           '20220524D', # spont.APs, evoked APs, fastevents     !recorded at RT
           '20220525A', #   fastevents (but only in the first 10 min. of an hour's worth of recording)
           '20220525B', # no spont.APs, evoked APs, not sure about fastevents (dozen events with amp 3-5mV)
           '20220525C', # no spont.APs, evoked APs, not sure about fastevents (four events with amp just >3mV)
           '20220525D', # spont.APs, evoked APs, fastevents
           '20220525E', # spont.APs, evoked APs, fastevents
           '20220525F', # spont.APs, evoked APs, fastevents
           '20220525G', # no spont.APs, evoked APs, no fastevents
           '20220531A1',
           '20220531B',
           '20220531C',
           ]

neurons_noQX = ['20220525A', '20220525D', '20220525E', '20220525F', '20220531A1', '20220531B',]

neurons_QX_noQXtip = ['20220531C']

neurons_QX = ['20220524A', '20220524B', '20220524C', '20220524D', '20220524E', '20220525B', '20220525C', '20220525G']

# getting depolarizing events for all neurons with standard extraction parameters (I want to see also spikelets and determine if their frequency goes down over the course of recordings)
# for neuron in neurons:
#     neuron_data = SingleNeuron(neuron)
#     neuron_data.get_depolarizingevents_fromrawdata()
#     neuron_data.write_results()
# %% seeing APs (and fastevents if there are any)
for neuron in neurons:
    neuron_data = SingleNeuron(neuron)
    if len(neuron_data.depolarizing_events) > 0:
        des_df = neuron_data.depolarizing_events
        aps_spont = des_df.event_label == 'actionpotential'
        aps_evoked = des_df.event_label == 'actionpotential_on_currentpulsechange'
        fastevents = (des_df.amplitude > 3) & (des_df.rise_time_20_80 < 2) & des_df.event_label.isna()
        # neuron_data.plot_depoleventsgroups_overlayed(aps_evoked, aps_spont, fastevents,
        #                                              group_labels=['spontAPs', 'evokedAPs', 'fastevents'])
        neuron_data.plot_depolevents(aps_spont,
                                     colorby_measure='width_50',
                                     do_baselining=False,
                                     prealignpoint_window_inms=50,
                                     plotwindow_inms=75,
                                     plt_title='spont APs')
        neuron_data.plot_depolevents(aps_evoked,
                                     colorby_measure='width_50',
                                     do_baselining=False,
                                     prealignpoint_window_inms=50,
                                     plotwindow_inms=75,
                                     plt_title='evoked APs')
        neuron_data.plot_depolevents(fastevents,
                                     colorby_measure='width_50',
                                     do_baselining=False,
                                     prealignpoint_window_inms=50,
                                     plotwindow_inms=75,
                                     plt_title='things that could be fastevents')

# %%
neuron_data = SingleNeuron('20220525G')
# neuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)
if len(neuron_data.depolarizing_events) > 0:
    des_df = neuron_data.depolarizing_events
    aps_spont = des_df.event_label == 'actionpotential'
    aps_evoked = des_df.event_label == 'actionpotential_on_currentpulsechange'
    fastevents = (des_df.amplitude > 3) & (des_df.rise_time_20_80 < 2) & des_df.event_label.isna()
    # neuron_data.plot_depoleventsgroups_overlayed(aps_evoked, aps_spont, fastevents,
    #                                              group_labels=['spontAPs', 'evokedAPs', 'fastevents'])
    neuron_data.plot_depolevents(aps_spont,
                                 colorby_measure='baselinev',
                                 do_baselining=False,
                                 prealignpoint_window_inms=50,
                                 plotwindow_inms=75,
                                 plt_title='spont APs')
    neuron_data.plot_depolevents(aps_evoked,
                                 colorby_measure='baselinev',
                                 do_baselining=False,
                                 prealignpoint_window_inms=50,
                                 plotwindow_inms=75,
                                 plt_title='evoked APs')
    neuron_data.plot_depolevents(fastevents,
                                 colorby_measure='baselinev',
                                 do_baselining=False,
                                 prealignpoint_window_inms=50,
                                 plotwindow_inms=75,
                                 plt_title='things that could be fastevents')

