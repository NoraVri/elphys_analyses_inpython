import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20190729A'
singleneuron_data = SingleNeuron(neuron_name)

# notes summary:
# almost an hour and a half of recording, and then another ~40min. of recording with excitatory inputs blocked.
# Nice and stable recording for the most part, with the cell moving back and forth between osc and non-osc states.
# Looks to be completely devoid of fast-events: my eyes don't see any events >~0.5mV amp, and all things that are
# clearly events (and not just noise) all look like spikelets.
# Interestingly, it seems relatively easy to get this neuron to fire APs using depolarizing DC (multiple evoked spikes
# on depol.steps in long-pulse recordings).

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'
# !no fast-events detected anywhere.
# %% analysis summary figures:
# parameter distributions of candidate fast-events (=events that are so far still unlabeled)
unlabeled_events = des_df.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
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
# des_df.loc[fast_events,'amplitude'].plot.hist(bins=30)
# plt.figure()
# des_df.loc[:,'rise_time_20_80'].plot.hist(bins=30)
# des_df.loc[fast_events,'rise_time_20_80'].plot.hist(bins=30)


# ongoing analysis notes:
#

# %% labeling of selected events: things that are definitely NOT fast-events
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
singleneuron_data.plot_depolevents(aps,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=20,
                                   plotwindow_inms = 100)

# %% quick check for any places where obvious noise-events have been detected
singleneuron_data.plot_rawdatablocks(events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))

# %% labeling noise-events etc.
noiseevents_candidates = (des_df.baselinev > -35) & (des_df.amplitude < 1)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      possibly_noise=noiseevents_candidates)
singleneuron_data.plot_depolevents(noiseevents_candidates,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )

# there is a single currentpulsechange that did not get labeled as such - doing it manually:
# singleneuron_data.depolarizing_events.loc[(des_df.amplitude>10)&(unlabeled_events),
#                                           'event_label'] = 'currentpulsechange'
# singleneuron_data.write_results()
# des_df = singleneuron_data.depolarizing_events


# %% labeling of selected events: things that could be fast-events
fastevents_largerthan_params = {
                                'amplitude':0.75,
                                # 'rise_time_20_80':0.2,
                                }
fastevents_smallerthan_params = {
                                 'rise_time_20_80': 2,
                                 'width_50': 20,
                                 'baselinev': -40
                                 }
fastevents_candidates = unlabeled_events
for key, value in fastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] > value)
for key, value in fastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] < value)

singleneuron_data.plot_depolevents(fastevents_candidates,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   prealignpoint_window_inms=10,
                                   plotwindow_inms=30,
                                   plt_title='possibly fast-events')
# I see just one event that MIGHT be fast enough to qualify as a fast-event, but it's in a pretty noisy trace
# so I don't trust it enough to classify as such. And anyway just one single event is of no use.

# %% labeling fast-events as such, and saving the data table
singleneuron_data.depolarizing_events.loc[fastevents_candidates, 'event_label'] = 'fastevent'
singleneuron_data.write_results()
des_df = singleneuron_data.depolarizing_events

