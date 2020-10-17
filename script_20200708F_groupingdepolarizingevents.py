import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20200708F'
singleneuron_data = SingleNeuron(neuron_name)

# a super relevant recording: Thy1-evoked excitations, also with application of AP5
# there's about 15 min. of recording without blocker, and then almost an hour with;
# early on, the neuron is mostly just going in and out of oscillating (small and large amp), but
# later on it starts doing spikes and fast-events vigorously
# !Note: it's the cell that just won't die, but that doesn't mean its unaffected by drift - there are periods where
# it's definitely not all that healthy, and bridge issues etc. may play up
# Interestingly, there are some light-evoked responses that are right around the amplitude criterion for APs,
# yet don't seem to have a shoulder at all and look much more like a fast-event instead...
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
aps = singleneuron_data.depolarizing_events.event_label == 'actionpotential'
spikeshoulderpeaks = singleneuron_data.depolarizing_events.event_label == 'spikeshoulderpeak'
# %% plotting this in parts, make sure to close plots in between or memory will run out
singleneuron_data.plot_rawdatablocks('gapFree', events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
# %%
singleneuron_data.plot_rawdatablocks('light', events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
# %%
lightevoked_aps = aps & singleneuron_data.depolarizing_events.applied_ttlpulse
spontaneous_aps = aps & ~singleneuron_data.depolarizing_events.applied_ttlpulse
singleneuron_data.plot_depolevents(spontaneous_aps,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms = 30,
                                   plt_title='spontaneous APs')

singleneuron_data.plot_depolevents(lightevoked_aps,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms = 30,
                                   plt_title='light evoked APs')
# the light-evoked 'APs' really look A LOT more like fast-events: they have no shoulder (except for two that occur at baselinev > -45mV),
# seem to come in amplitude-groups, and decay faster for lower baselinev

# %% removing AP label from large-amp light-evoked responses without shoulder:
# non_ap_evokedevents = lightevoked_aps&(singleneuron_data.depolarizing_events.baselinev<-43)
# singleneuron_data.depolarizing_events.loc[non_ap_evokedevents,'event_label'] = None
# singleneuron_data.write_results()
# %% quick check: all events that do not (yet) have labels are subthreshold depolarizing events
currentpulsechanges = singleneuron_data.depolarizing_events.event_label == 'currentpulsechange'
singleneuron_data.plot_rawdatablocks('gapFree', events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))
# %%
singleneuron_data.plot_rawdatablocks('light', events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))

# if there are any events that are obviously noise, label them as such
# there are rather many 'events' in the stretches of recording where this neuron is behaving rather noisily,
# but they do tend to be rather small (naked eye says fast-events are 2mV amp and up, while noise-events are ~1mV)


# %% looking at parameter distributions of detected subthreshold depolarizations
# (i.e., all events that do not yet have a label)

unlabeled_events = singleneuron_data.depolarizing_events.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~singleneuron_data.depolarizing_events.applied_ttlpulse
evoked_unlabeled_events = unlabeled_events & singleneuron_data.depolarizing_events.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      evoked_depols=evoked_unlabeled_events)

# %% plotting groups of events baselined&normalized
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
# singleneuron_data.write_results()
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