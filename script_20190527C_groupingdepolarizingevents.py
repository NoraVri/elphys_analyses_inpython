import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20190527C'
singleneuron_data = SingleNeuron(neuron_name)


# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
aps = singleneuron_data.depolarizing_events.event_label == 'actionpotential'
spikeshoulderpeaks = singleneuron_data.depolarizing_events.event_label == 'spikeshoulderpeak'

singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks))

singleneuron_data.plot_depolevents(aps,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=20,
                                   plotwindow_inms = 200)

# %% quick check: all events that do not (yet) have labels are subthreshold depolarizing events
currentpulsechanges = singleneuron_data.depolarizing_events.event_label == 'currentpulsechange'
singleneuron_data.plot_rawdatablocks(events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))

# if there are any events that are obviously noise, label them as such



# %% looking at parameter distributions of detected subthreshold depolarizations
# (i.e., all events that do not yet have a label)

unlabeled_events = singleneuron_data.depolarizing_events.event_label.isna()
singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
                                                      cmeasure='baselinev',
                                                      subthreshold_depolarizations=unlabeled_events)

# %% plotting groups of events baselined&normalized
# neuron20190527C: -80 < baselinev < -30, amplitude > 2, rise_time < 2
fastevents_largerthan_params = {
                                'amplitude':0.5,
                                # 'baselinev':-80,
                                }
fastevents_smallerthan_params = {
                                 'rise_time_20_80': 0.7,
                                 }
fastevents_candidates = unlabeled_events
for key, value in fastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (singleneuron_data.depolarizing_events[key] > value)
for key, value in fastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (singleneuron_data.depolarizing_events[key] < value)

singleneuron_data.plot_depolevents(fastevents_candidates,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   prealignpoint_window_inms=10,
                                   plotwindow_inms=30,
                                   plt_title='presumably all fast-events')

# %% labeling fast-events as such, and saving the data table
singleneuron_data.depolarizing_events.event_label[fastevents_candidates] = 'fastevent'
singleneuron_data.write_results()
# tinyfastevents_largerthan_params = {
#                                 'amplitude':0.4,
#                                 # 'baselinev':-80,
#                                 }
# tinyfastevents_smallerthan_params = {
#                                  'rise_time_20_80': 0.2,
#                                  }
# tinyfastevents_candidates = unlabeled_events
# for key, value in fastevents_largerthan_params.items():
#     tinyfastevents_candidates = tinyfastevents_candidates & (singleneuron_data.depolarizing_events[key] > value)
# for key, value in fastevents_smallerthan_params.items():
#     tinyfastevents_candidates = tinyfastevents_candidates & (singleneuron_data.depolarizing_events[key] < value)
# singleneuron_data.plot_depolevents((fastevents_candidates | tinyfastevents_candidates),
#                                    colorby_measure='baselinev',
#                                    do_baselining=True,
#                                    # do_normalizing=True,
#                                    prealignpoint_window_inms=10,
#                                    plotwindow_inms=30,
#                                    plt_title='presumably all fast-events')