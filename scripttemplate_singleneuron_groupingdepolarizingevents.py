import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron
singleneuron_data = SingleNeuron('20190814A')


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





# %% a quick look to see if we can isolate fast-events from among all depolarizations
# neuron20190527A: baselinev < -25, amplitude > 1.5, rise_time < 1
# neuron20190527C: -80 < baselinev < -30, amplitude > 2, rise_time < 2
# neuron20190529B: amplitude > 1 - basically all evoked responses look like stacked fast-events
# neuron20190529D: amplitude > 3, rise_time < 2 - but also: amplitude > 0.5, rise_time < 0.3
# neuron20190529E: amplitude > 0.4, rise_time < 0.5

# fastevents_largerthan_params = {
#                                 'amplitude':3,
#                                 # 'baselinev':-80,
#                                 }
# fastevents_smallerthan_params = {
#                                  'baselinev':-25,
#                                  'rise_time':1,
#                                  }
#
# possiblyfastevents_spont = spont_events
# possiblyfastevents_evoked = evoked_events
# for key, value in fastevents_largerthan_params.items():
#     possiblyfastevents_spont = (possiblyfastevents_spont
#                                 & (singleneuron_data.depolarizing_events[key] > value))
#     possiblyfastevents_evoked = (possiblyfastevents_evoked
#                                  & (singleneuron_data.depolarizing_events[key] > value))
# for key, value in fastevents_smallerthan_params.items():
#     possiblyfastevents_spont = (possiblyfastevents_spont
#                                 & (singleneuron_data.depolarizing_events[key] < value))
#     possiblyfastevents_evoked = (possiblyfastevents_evoked
#                                  & (singleneuron_data.depolarizing_events[key] < value))
#
# singleneuron_data.plot_depolevents_overlayed(possiblyfastevents_spont,
#                                              colorby_measure='baselinev',
#                                              do_baselining=True,
#                                              # do_normalizing=True,
#                                              prealignpoint_window_inms=10,
#                                              total_plotwindow_inms=25,
#                                              # newplot_per_block=True,
#                                              # blocknames_list=['light_wholeField_0009.abf']
#                                              )
#
#
# singleneuron_data.plot_depolevents_overlayed(possiblyfastevents_evoked,
#                                              colorby_measure='baselinev',
#                                              do_baselining=True,
#                                              do_normalizing=True,
#                                              prealignpoint_window_inms=10,
#                                              total_plotwindow_inms=25,
#                                              )
# plt.suptitle('evoked events')
#
# singleneuron_data.plot_depoleventsgroups_overlayed(possiblyfastevents_spont,
#                                                    possiblyfastevents_evoked,
#                                                    group_labels=['spontaneous', 'evoked'],
#                                                    # blocknames_list=blocksnames_list,
#                                                    do_baselining=True, do_normalizing=True,
#                                                    plt_title='presumably all fast-events')
