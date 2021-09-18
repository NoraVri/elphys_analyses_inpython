# %% imports
from singleneuron_class import SingleNeuron
import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

# metadata imports
path="D:\\hujigoogledrive\\research_YaromLabWork\\data_elphys_andDirectlyRelatedThings\\recorded_by_me"
recordings_metadata = pd.read_csv(path+'\\'+'myData_recordings_metadata.csv')
experimentdays_metadata = pd.read_csv(path+'\\'+'myData_experimentDays_metadata.csv')

# list of neuron recordings to work with, as found in script_depolarizingevents_dataset: (>30min. recording at PT, and high frequency of fast-events by eye)
frequent_fastevents_neurons = [
'20190331A1', #-for one compound event, was able to subtract the smaller first peak and get a larger, single fast-event
'20190331A2', #
'20190401A1', #
'20190401B1', #
'20190410A2', #
'20190527A',  #
'20190805A2', #
'20190812A',  # fast-events sorted, neat events selecting still to do
'20190815C',  # fast-events sorted, neat events selecting still to do
# '20200708F',  # events partially sorted
'20210113H',  # fast-events sorted, neat events selecting still to do
# '20210124A',  # events not yet sorted
]

# %% histograms of events parameters

# all events, split out by category (AP, fastevent, compound_event, smallslowevent)

eventstypes_list = ['ap', 'fastevent', 'compound_event', ]
parameters_forplotting = {'amplitude': [-1, 25, 100],  #binlims min, binlims max, ###--not working yet-- max count (y axis limit)
                          'rise_time_20_80': [0, 5, 100],
                          'width_50': [0, 10, 100],
                          'maxdvdt': [0, 10, 100],
                          'baselinev': [-80, -15, 100],
                          }
binsize = 0.1
plot_smallslowevents = False


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




