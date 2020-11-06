import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20200818B'
singleneuron_data = SingleNeuron(neuron_name)

# notes summary:
# at first glance it's pretty clear what are the fast events - there's a few groups with amp between 9 - 12 mV,
# and another group with amp ~5mV. But then I plot them normalized and they're just not entirely identical enough...

des_df = singleneuron_data.depolarizing_events
aps = (des_df.event_label == 'actionpotential') | (des_df.event_label == 'actionpotential_on_currentpulsechange')
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'

# analysis summary figures:
# parameter distributions of candidate fast-events (=events that are so far still unlabeled)
unlabeled_events = des_df.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
# evoked_unlabeled_events = unlabeled_events & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      # evoked_depols=evoked_unlabeled_events
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      # evoked_depols=evoked_unlabeled_events
                                                      )

# fast_events = des_df.event_label == 'fastevent'
# other_fast_events = des_df.event_label == 'otherfastevent'
# singleneuron_data.plot_depolevents(fast_events,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='amplitude',  # colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
# singleneuron_data.plot_depolevents(other_fast_events,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='amplitude',  # colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
# plt.figure()
# des_df.loc[:,'amplitude'].plot.hist(bins=30)
# plt.title('all events, amplitude')
# plt.figure()
# des_df.loc[fast_events,'amplitude'].plot.hist(bins=15)
# plt.title('fast-events, amplitude')
# plt.figure()
# des_df.loc[fast_events,'rise_time_20_80'].plot.hist(bins=15)
# plt.title('fast events, rise-time (20-80%amp)')
# plt.figure()
# des_df.loc[fast_events, 'width_50'].plot.hist(bins=15)
# plt.title('fast events, half-width')


# ongoing analysis notes:
#

# %% labeling of selected events: things that are definitely NOT fast-events
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
singleneuron_data.plot_depolevents((aps & ~des_df.applied_ttlpulse),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=30,
                                   plotwindow_inms = 100,
                                   plt_title='spontaneous APs')

singleneuron_data.plot_depolevents((aps & des_df.applied_ttlpulse),
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=30,
                                   plotwindow_inms = 100,
                                   plt_title='light-evoked APs')


# %% quick check for any places where obvious noise-events have been detected
singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_events)

# %% labeling noise-events etc.
# there's bound to be noise in the small events, and there are definitely some things that are not events but
# just the neuron being happy - but it all happens in the range of small amplitudes (1mV or so) so I don't think
# it's worth cleaning up right now.





# %% labeling of selected events: things that could be fast-events
# I looked for, but didn't find any events <1mV amp that have a waveform corresponding to the larger-amp fast-events.
#
fastevents_largerthan_params = {
                                'amplitude':1,
                                # 'baselinev':-80,
                                }
fastevents_smallerthan_params = {
                                 'rise_time_20_80': 2,
                                 }
fastevents_candidates = unlabeled_events
for key, value in fastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] > value)
for key, value in fastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] < value)

singleneuron_data.plot_depolevents(fastevents_candidates,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   prealignpoint_window_inms=10,
                                   plotwindow_inms=30,
                                   plt_title='presumably all fast-events')

# %% labeling fast-events as such, and saving the data table
singleneuron_data.depolarizing_events.loc[fastevents_candidates, 'event_label'] = 'fastevent'
singleneuron_data.write_results()
des_df = singleneuron_data.depolarizing_events

