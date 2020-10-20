import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20190529C'
singleneuron_data = SingleNeuron(neuron_name)

# notes summary:
# there's about 13 min. of recording altogether, but only about 5 min. really before the neuron dies; holding on to it
# with lots of -DC (down to -1.5nA) and there is basically no visible response to light at all (except in that one
# trace where there's a clear spikelet during the light pulse, and about 200 ms later the neuron does some
# wacky oscillating for a few s).


des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'

# analysis summary figures:
# parameter distributions of candidate fast-events (=events that are so far still unlabeled)
unlabeled_events = des_df.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
# evoked_unlabeled_events = unlabeled_events & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      # evoked_depols=evoked_unlabeled_events
                                                      )
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
singleneuron_data.scatter_depolarizingevents_measures('width_30', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      # evoked_depols=evoked_unlabeled_events
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('width_10', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      # evoked_depols=evoked_unlabeled_events
                                                      )
fast_events = des_df.event_label == 'fastevent'
singleneuron_data.plot_depolevents(fast_events,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   colorby_measure='amplitude',  # colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )

plt.figure()
des_df.loc[:,'amplitude'].plot.hist(bins=30)
plt.title('all events, amplitude')
plt.figure()
des_df.loc[fast_events,'amplitude'].plot.hist(bins=15)
plt.title('fast-events, amplitude')
plt.figure()
des_df.loc[fast_events,'rise_time_20_80'].plot.hist(bins=15)
plt.title('fast events, rise-time (20-80%amp)')
plt.figure()
des_df.loc[fast_events, 'width_50'].plot.hist(bins=15)
plt.title('fast events, half-width')


# ongoing analysis notes:
# the tiny events (<1mV) are small and numerous, and there's a lot of variability there that looks normally distributed;
# but I'm quite convinced that it's not coincidence that there are some that have the same rise and decay as the larger
# fast-events; the small group really is also visible in the scatters (although it did take looking at three different
# width measures scatters to convince myself)

# %% labeling of selected events: things that are definitely NOT fast-events
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
singleneuron_data.plot_rawdatablocks(events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
singleneuron_data.plot_depolevents(aps,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=20,
                                   plotwindow_inms=150)

# %% quick check for any places where obvious noise-events have been detected
singleneuron_data.plot_rawdatablocks(events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))

# %% labeling noise-events etc.
# there are a couple of things that got picked up as events large enough to interfere with finding fast-events by amp,
# but are actually just the neuron oscillating a bit; it happens exclusively at baselinev -43 - -40mV, so
# labeling those as noise-events:
noiseevents_candidates = ((des_df.baselinev > -43) & (des_df.baselinev < -40)
                          & (des_df.rise_time_20_80 < 2)
                          & (des_df.amplitude > 1) & (des_df.amplitude < 3))
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      possibly_noise=noiseevents_candidates)
singleneuron_data.plot_depolevents(noiseevents_candidates,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# singleneuron_data.depolarizing_events.loc[noiseevents_candidates, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# des_df = singleneuron_data.depolarizing_events
# %%
# found some more:
noiseevents_candidates = (unlabeled_events & (des_df.amplitude > 2.5) & (des_df.rise_time_20_80 > 2))
singleneuron_data.plot_depolevents(noiseevents_candidates,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# singleneuron_data.depolarizing_events.loc[noiseevents_candidates, 'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# des_df = singleneuron_data.depolarizing_events

# %% labeling of selected events: things that could be fast-events
# first, let's label all things that are definitely fast-events (cause it looks like there are some that are <1mV amp,
# but to see that I'll have to use narrower criteria than what keeps all the big ones in the group)
fastevents_largerthan_params = {
                                'amplitude': 0.75,
                                'width_30':6,
                                'width_10': 9,
                                }
fastevents_smallerthan_params = {
                                 'width_30': 8,
                                 'rise_time_20_80': 1.6,
                                 }
fastevents_candidates = spont_unlabeled_events
for key, value in fastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] > value)
for key, value in fastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] < value)

singleneuron_data.plot_depolevents(fastevents_candidates,
                                   colorby_measure='amplitude',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   prealignpoint_window_inms=10,
                                   plotwindow_inms=30,
                                   plt_title='presumably all fast-events')
# the small ones are definitely noisier, but they look pretty darned the same in rise and decay as the big ones...
# %% labeling fast-events as such, and saving the data table
singleneuron_data.depolarizing_events.loc[fastevents_candidates, 'event_label'] = 'fastevent'
singleneuron_data.write_results()
des_df = singleneuron_data.depolarizing_events



