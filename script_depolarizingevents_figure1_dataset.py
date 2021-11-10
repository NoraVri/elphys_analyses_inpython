# %% imports
import os

from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import quantities as pq
import pandas as pd

# metadata imports
path="D:\\Beaste_IIa_Documents_backup\\elphys_andDirectlyRelatedThings_copy"
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
'20190331A1', #! there's a pattern to the neat double-events (of which there are lots) and the second peak in double-events looks different from the first. Also, APs usually have a triple up-stroke.
'20190331A2', # very few double-events, the 4 'neat' ones that are there all look different from each other. APs all seem to have a double or triple up-stroke.
'20190401A1', # very few double-events, the 4 'neat' ones that are there all look different from each other. APs all seem to have a triple up-stroke.
'20190401B1', # very few double-events, only a single 'neat' one. APs all seem to have double or triple up-stroke.
'20190410A2', # only a single double-event, even that one doubtful; relatively few fast-events, too. APs have single (evoked during +DC) or double up-stroke.
'20190527A',  # a handful of double-events, all (except one) occurring late in the recording under deteriorated conditions. AP up-strokes have at least two, up to 4 or 5 phases.
'20190805A2', # clear example of a neuron with large-amp fast-events that are seen only at more hyperpolarized baselinev, because otherwise they evoke AP. Only one compound event in the whole entire recording, and it's definitely more like a failed AP (amp 40mV, though no shoulder). AP up-strokes have all the kinds of shapes I've seen so far.
'20190812A',  # only a single double-event in the whole recording, even then doubtful - it stands out mostly by amplitude.
'20190815C',  # handful of double-events occurring only during a specific time in the recording; no APs at all.
'20200708F',  #! double-events don't start appearing until well after AP5 application; APs all have double or triple up-stroke
'20210113H',  # no double-events really, but triple - but not until very late into recordings after axons were tortured with light a bunch. APs all have double up-stroke.
'20210124A',  #! has double events sporadically throughout the recording, but most concentratedly during periods with -DC and no APs; for one of the more common events, double-event - single-event = single-event, it looks like. APs all have double or triple up-stroke.
]
# %%
frequent_fastevents_neurons_ampgroups = [
    ('20190331A1', 3),
    ('20190331A2', 3),
    ('20190401A1', 3),
    ('20190401B1', 3),
    ('20190410A2', 2),
    ('20190527A', 5),
    ('20190805A2',3),
    ('20190812A',4),
    ('20190815C',3),
    ('20200708F',3),
    ('20210113H',4),
    ('20210124A',4),
]
ampgroups_df = pd.DataFrame(frequent_fastevents_neurons_ampgroups)
ampgroups_df.hist(column=1)

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

# %% one plot for all neurons: histograms of averaged events' parameters
for neuron in frequent_fastevents_neurons:
    des_df = pd.read_csv()

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
# %% seeing all double events for each neuron
for neuron in frequent_fastevents_neurons:
    neuron_data = SingleNeuron(neuron)
    neuron_data.plot_depolevents((neuron_data.depolarizing_events.event_label == 'compound_event'),
                                 colorby_measure='baselinev',
                                 do_baselining=True,
                                 # do_normalizing=True,
                                 plotwindow_inms=15,
                                 plt_title=' neat compound events'
                                 )
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
                                   prealignpoint_window_inms=2,
                                   plotwindow_inms=25,
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



