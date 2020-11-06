import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron
# %%
neuron_name = '20190529A1'
singleneuron_data = SingleNeuron(neuron_name)
# %%
# notes summary:
# has spntaneous fast-events with decently large amplitude, as well as some with small amplitude (1 - 3 mV)
# and spikelets of similar size (left off working on carefully selecting the parameters of the smaller fast events).

des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'

# analysis summary figures:
# parameter distributions of candidate fast-events (=events that are so far still unlabeled)
unlabeled_events = des_df.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
evoked_unlabeled_events = unlabeled_events & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      evoked_depols=evoked_unlabeled_events
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      evoked_depols=evoked_unlabeled_events
                                                      )

fast_events = des_df.event_label == 'fastevent'
# other_fast_events = des_df.event_label == 'otherfastevent'
singleneuron_data.plot_depolevents(fast_events,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   colorby_measure='amplitude',  # colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# singleneuron_data.plot_depolevents(other_fast_events,
#                                    do_baselining=True,
#                                    do_normalizing=True,
#                                    colorby_measure='amplitude',  # colorby_measure='baselinev',
#                                    prealignpoint_window_inms=5,
#                                    plotwindow_inms=30,
#                                    )
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
# interestingly, the spont. and light-evoked APs look VERY similar - there just seem to be more in the spont. group.

# %% quick check for any places where obvious noise-events have been detected
singleneuron_data.plot_rawdatablocks(events_to_mark=unlabeled_events)

# in the first recording file (gapFree_0000) it seems that the neuron is not actually so well patched initially
# (very high apparent 'Rin') but it gets fixed at about 471s into the recording.
# labeling all events that happen before that as 'noise':
# sr = float(singleneuron_data.blocks[0].segments[0].analogsignals[0].sampling_rate)
# trace_start_t = singleneuron_data.rawdata_readingnotes['nonrecordingtimeslices']['gapFree_0000.abf']['t_start']
# noise_end_idx = (471 - trace_start_t) * sr
# noisy_events = (des_df.file_origin == 'gapFree_0000.abf') & (des_df.peakv_idx < noise_end_idx)
# singleneuron_data.depolarizing_events.loc[noisy_events, 'event_label'] = 'noiseevent'
# everything else looks to be in the clear
# singleneuron_data.write_results()


# %% labeling of selected events: things that could be fast-events
# there's a group of events with amp > 3mV and rise-time < 1ms that are definitely fast-events;
# amplitude-groups aren't very clear, but probably there, and normalized decays are identical.
# There are a few more small fast-events (up to 3mV amp) occurring at baselinev ~-35mV that have the same norm. decay
# (faster than events occurring at lower baselinev) and event of ~12mV amp that clearly compound (rise-time a little >1ms)
# but still clearly has the decay-shape that is expected at that baselinev.

fastevents_largerthan_params = {
                                'amplitude': 0.75,
                                'rise_time_20_80': 0.3,
                                }
fastevents_smallerthan_params = {
                                 'rise_time_20_80': 0.65,
                                 'width_50': 2.5,
                                 }
fastevents_candidates = unlabeled_events & ~des_df.applied_ttlpulse
for key, value in fastevents_largerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] > value)
for key, value in fastevents_smallerthan_params.items():
    fastevents_candidates = fastevents_candidates & (des_df[key] < value)
# %%
singleneuron_data.plot_depolevents(fastevents_candidates,
                                   colorby_measure='baselinev',
                                   do_baselining=True,
                                   do_normalizing=True,
                                   prealignpoint_window_inms=10,
                                   plotwindow_inms=30,
                                   plt_title='presumably all fast-events')

# %% labeling fast-events as such, and saving the data table
# all spont. events with amp > 2mV have been labeled as fast-events;
# now further selecting smaller-amp ones by amp, rise-time and width (still in progress)
singleneuron_data.depolarizing_events.loc[fastevents_candidates, 'event_label'] = 'fastevent'
singleneuron_data.write_results()

