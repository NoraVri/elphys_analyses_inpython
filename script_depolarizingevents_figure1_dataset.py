# %% imports
import os

from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import quantities as pq
import pandas as pd

# metadata imports
path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

# list of neuron recordings to work with, as found in script_depolarizingevents_dataset: (>30min. recording at PT,
# and high frequency of fast-events by eye).
# Analysis procedure for each of these neurons:
# - extracting depolarizing events, tweaking algorithm parameter settings to extract as small as possible events
# - sorting through all depolarizing events and labeling fast-events and compound-events (and any obvious noise-events encountered along the way)
# - selecting 5 min. of recording time that best represents the neuron's typical behavior, and marking events
#   occurring there as 'neat'
frequent_fastevents_neurons = [
'20190331A1', # fast-events sorted, neat events selected, summary plots done; also did some plots of averaged events, and started playing with compound events
'20190331A2', # fast-events sorted, neat events selected, summary plots done; also did some plots of averaged events, but haven't done anything yet with compound events but there are lots
'20190401A1', # fast-events sorted, neat events selected, summary plots done; also did some plots of averaged events, and started playing with compound events
'20190401B1', # fast-events sorted, neat events selected, summary plots done; did one plot of averaged events
'20190410A2', # fast-events sorted, neat events selected, summary plots done
'20190527A',  # fast-events sorted, neat events selected, summary plots done
'20190805A2', # fast-events sorted, neat events selected, summary plots done
'20190812A',  # fast-events sorted, neat events selected, summary plots done
'20190815C',  # fast-events sorted, neat events selected, summary plots done
'20200708F',  # fast-events sorted, neat events selected, summary plots done
'20210113H',  # fast-events sorted, neat events selected, summary plots done
'20210124A',  # fast-events sorted, neat events selected, summary plots done
]


# %% histograms of events parameters

# all events, split out by category (AP, fastevent, compound_event, smallslowevent)
# for each neuron in the list, one figure showing parameters for all events, and one showing only 'neat' ones
# (if those have been marked).
eventstypes_list = ['ap', 'fastevent', 'compound_event', ]
colors_list = ['r', 'b', 'g']
parameters_forplotting = {'amplitude': [-1, 25, 100],  #binlims min, binlims max, ###--not working yet-- max count (y axis limit)
                          'rise_time_20_80': [0, 5, 100],
                          'width_50': [0, 10, 100],
                          'maxdvdt': [0, 10, 100],
                          'baselinev': [-80, -15, 100],
                          }
binsize = 0.1
plot_smallslowevents = False

# %% three figures for each neuron: line plot of neat events, histograms of neat events and histograms of all events
for neuron in frequent_fastevents_neurons:
    neuron_data = SingleNeuron(neuron)
    # line plot of neat fast-events, if neat events have been marked
    if 'neat_event' in neuron_data.depolarizing_events.columns:
        events_to_plot = ((neuron_data.depolarizing_events.neat_event)
                          & (neuron_data.depolarizing_events.event_label == 'fastevent'))
        neuron_data.plot_depolevents(events_to_plot,
                                     colorby_measure='baselinev',
                                     plotwindow_inms=20,
                                     )
    # histograms of neat events only
        i = 0
        figure, axes = plt.subplots(len(parameters_forplotting), 1)
        figure.suptitle(neuron_data.name)
        for parameter, hist_edges in parameters_forplotting.items():
            parameter_data = neuron_data.depolarizing_events.loc[neuron_data.depolarizing_events.neat_event, parameter]
            parameter_bins = np.linspace(hist_edges[0], hist_edges[1],
                                         num=(int((hist_edges[1] - hist_edges[0]) / binsize) + 1))
            for eventstype in eventstypes_list:
                eventsgroup_data = parameter_data[neuron_data.depolarizing_events.event_label == eventstype]
                axes[i].hist(eventsgroup_data, bins=parameter_bins, alpha=0.3, label=eventstype)
            if plot_smallslowevents:
                unlabeledspontevents_data = parameter_data[(neuron_data.depolarizing_events.event_label.isna()
                                                            & ~neuron_data.depolarizing_events.applied_ttlpulse)]
                axes[i].hist(unlabeledspontevents_data, bins=parameter_bins, alpha=0.7, label='unlabeled spont.events')
            axes[i].set_title(parameter + ' neat events only')
            # axes[i].set_ylim(0, parameter_bins[2])
            i += 1
        axes[0].legend()
    # histograms of all events' parameters
    i = 0
    figure, axes = plt.subplots(len(parameters_forplotting), 1)
    figure.suptitle(neuron_data.name)
    for parameter, hist_edges in parameters_forplotting.items():
        parameter_data = neuron_data.depolarizing_events[parameter]
        parameter_bins = np.linspace(hist_edges[0], hist_edges[1],
                                     num=(int((hist_edges[1] - hist_edges[0]) / binsize) + 1))
        for eventstype in eventstypes_list:
            eventsgroup_data = parameter_data[neuron_data.depolarizing_events.event_label == eventstype]
            axes[i].hist(eventsgroup_data, bins=parameter_bins, alpha=0.3, label=eventstype)
        if plot_smallslowevents:
            unlabeledspontevents_data = parameter_data[(neuron_data.depolarizing_events.event_label.isna()
                                                        & ~neuron_data.depolarizing_events.applied_ttlpulse)]
            axes[i].hist(unlabeledspontevents_data, bins=parameter_bins, alpha=0.5, label='unlabeled spont.events')
        axes[i].set_title(parameter)
        # axes[i].set_ylim(0, parameter_bins[2])
        i += 1
    axes[0].legend()

# %% two figures for each neuron: line plot of neat events, histograms of neat events and all events overlayed
for neuron in frequent_fastevents_neurons:
    neuron_data = SingleNeuron(neuron)
    # line plot of neat fast-events, if neat events have been marked
    if 'neat_event' in neuron_data.depolarizing_events.columns:
        events_to_plot = ((neuron_data.depolarizing_events.neat_event)
                          & (neuron_data.depolarizing_events.event_label == 'fastevent'))
        neuron_data.plot_depolevents(events_to_plot,
                                     colorby_measure='baselinev',
                                     plotwindow_inms=20,
                                     )
    # histograms of events parameters - all events and neat events overlayed
    i = 0
    figure, axes = plt.subplots(len(parameters_forplotting), 1)
    figure.suptitle(neuron_data.name)
    for parameter, hist_edges in parameters_forplotting.items():
        parameter_data = neuron_data.depolarizing_events[parameter]
        parameter_bins = np.linspace(hist_edges[0], hist_edges[1],
                                     num=(int((hist_edges[1] - hist_edges[0]) / binsize) + 1))
        j = 0
        for eventstype in eventstypes_list:
            eventsgroup_data = parameter_data[neuron_data.depolarizing_events.event_label == eventstype]
            axes[i].hist(eventsgroup_data, bins=parameter_bins, color=colors_list[j], alpha=0.3, label=eventstype)
            if 'neat_event' in neuron_data.depolarizing_events.columns:
                neateventsgroup_data = parameter_data[(neuron_data.depolarizing_events.event_label == eventstype)
                                                      & (neuron_data.depolarizing_events.neat_event)]
                axes[i].hist(neateventsgroup_data, bins=parameter_bins, color=colors_list[j], label=('neat ' + eventstype))
                j += 1
        if plot_smallslowevents:
            unlabeledspontevents_data = parameter_data[(neuron_data.depolarizing_events.event_label.isna()
                                                        & ~neuron_data.depolarizing_events.applied_ttlpulse)]
            axes[i].hist(unlabeledspontevents_data, bins=parameter_bins, color='c', alpha=0.5, label='unlabeled spont.events')
            if 'neat_event' in neuron_data.depolarizing_events.columns:
                neatunlabeledspontevents_data = parameter_data[(neuron_data.depolarizing_events.event_label.isna()
                                                                & ~neuron_data.depolarizing_events.applied_ttlpulse
                                                                & neuron_data.depolarizing_events.neat_event)]
                axes[i].hist(neatunlabeledspontevents_data, bins=parameter_bins, color='c', label=('neat unlabeled spont.events'))
        axes[i].set_title(parameter)
        i += 1
    axes[-1].legend()

# %% line plots
# getting a list of all neurons that have labeled fastevents
labeled_fastevents_neurons = []
results_path = path + '\\' + 'myResults'
depolarizingevents_tables = [file for file in os.listdir(results_path) if 'depolarizing_events' in file]
for table in depolarizingevents_tables:
    depolarizing_events = pd.read_csv((results_path + '\\' + table), index_col=0)
    if sum(depolarizing_events.event_label == 'fastevent') > 0:
        labeled_fastevents_neurons.append(table[:-24])
# %% one figure for frequent-fastevents neurons: neat fast-events normalized and averaged
from singleneuron_analyses_functions import get_events_average
figure, axes = plt.subplots(1, 2)
colormap = mpl.cm.Paired
cmnormalizer = mpl.colors.Normalize(0, len(frequent_fastevents_neurons))
for i, neuron in enumerate(frequent_fastevents_neurons):
    neuron_data = SingleNeuron(neuron)
    neuron_depolarizingevents = neuron_data.depolarizing_events
    neat_fastevents = ((neuron_depolarizingevents.event_label == 'fastevent') & (neuron_depolarizingevents.neat_event))
    normalized_neatfastevents_avg, \
    normalized_neatfastevents_std, \
    time_axis = get_events_average(neuron_data.blocks,
                                   neuron_data.depolarizing_events,
                                   neuron_data.rawdata_readingnotes['getdepolarizingevents_settings'],
                                   neat_fastevents,
                                   timealignto_measure='rt20_start_idx',
                                   plotwindow_inms=20,
                                   do_normalizing=True)
    linecolor = colormap(cmnormalizer(i))
    axes[0].plot(time_axis, normalized_neatfastevents_avg, linewidth=2.5, color=linecolor)
    axes[0].plot(time_axis, (normalized_neatfastevents_avg - normalized_neatfastevents_std), '--', color=linecolor)
    axes[0].plot(time_axis, (normalized_neatfastevents_avg + normalized_neatfastevents_std), '--', color=linecolor)
    axes[0].set_xlabel('time (ms)')
    diff_events_avg = np.diff(normalized_neatfastevents_avg)
    axes[1].plot(normalized_neatfastevents_avg[:-1:], diff_events_avg, color=linecolor, label=neuron_data.name)
    axes[1].set_xlabel('V')
    axes[1].set_ylabel('dV/dt')
    axes[1].legend(loc='upper left')

# %% one figure for all neurons with labeled fastevents: all fast-events normalized and averaged
from singleneuron_analyses_functions import get_events_average
figure, axes = plt.subplots(1, 2)
colormap = mpl.cm.tab20
cmnormalizer = mpl.colors.Normalize(0, len(labeled_fastevents_neurons))
for i, neuron in enumerate(labeled_fastevents_neurons):
    neuron_data = SingleNeuron(neuron)
    neuron_depolarizingevents = neuron_data.depolarizing_events
    fastevents = (neuron_depolarizingevents.event_label == 'fastevent')
    normalized_neatfastevents_avg, \
    normalized_neatfastevents_std, \
    time_axis = get_events_average(neuron_data.blocks,
                                   neuron_data.depolarizing_events,
                                   neuron_data.rawdata_readingnotes['getdepolarizingevents_settings'],
                                   fastevents,
                                   timealignto_measure='rt20_start_idx',
                                   plotwindow_inms=20,
                                   do_normalizing=True)
    linecolor = colormap(cmnormalizer(i))
    axes[0].plot(time_axis, normalized_neatfastevents_avg, linewidth=2.5, color=linecolor)
    axes[0].plot(time_axis, (normalized_neatfastevents_avg - normalized_neatfastevents_std), '--', color=linecolor)
    axes[0].plot(time_axis, (normalized_neatfastevents_avg + normalized_neatfastevents_std), '--', color=linecolor)
    axes[0].set_xlabel('time (ms)')
    diff_events_avg = np.diff(normalized_neatfastevents_avg)
    axes[1].plot(normalized_neatfastevents_avg[:-1:], diff_events_avg, color=linecolor, label=neuron_data.name)
    axes[1].set_xlabel('V')
    axes[1].set_ylabel('dV/dt')
    axes[1].legend(loc='upper left')

# %% generating a data table with statistics



