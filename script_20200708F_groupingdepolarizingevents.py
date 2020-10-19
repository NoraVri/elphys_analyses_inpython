import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd

from singleneuron_class import SingleNeuron

neuron_name = '20200708F'
singleneuron_data = SingleNeuron(neuron_name)

# notes summary:
# a super relevant recording: Thy1-evoked excitations, also with application of AP5
# there's about 15 min. of recording without blocker, and then almost an hour with;
# early on, the neuron is mostly just going in and out of oscillating (small and large amp), but
# later on it starts doing spikes and fast-events vigorously.
# !Note: it's the cell that just won't die, but that doesn't mean its unaffected by drift - there are periods where
# it's definitely not all that healthy, and bridge issues etc. may be playing up.


des_df = singleneuron_data.depolarizing_events
aps = des_df.event_label == 'actionpotential'
spikeshoulderpeaks = des_df.event_label == 'spikeshoulderpeak'
currentpulsechanges = des_df.event_label == 'currentpulsechange'
# parameter distributions of candidate fast-events (=events that are so far still unlabeled)
unlabeled_events = des_df.event_label.isna()
spont_unlabeled_events = unlabeled_events & ~des_df.applied_ttlpulse
evoked_unlabeled_events = unlabeled_events & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      evoked_depols=evoked_unlabeled_events)
singleneuron_data.scatter_depolarizingevents_measures('width_50', 'amplitude',
                                                      cmeasure='baselinev',
                                                      spont_subthreshold_depols=spont_unlabeled_events,
                                                      evoked_depols=evoked_unlabeled_events)
# ongoing analysis notes:
# well... That pretty much does not at all look like what we expect from a neuron that has only axonal fast-events.
# will definitely have to do some noise-cleanup to get a clearer view on parameter distributions of fast(er) events.
# Interestingly, there are some light-evoked responses that are right around the amplitude criterion for APs,
# yet don't seem to have a shoulder at all.
# The more I'm analyzing this data, the more it feels like this neuron's dendrites are slowly giving out
# over the course of recordings, while the axon keeps doing its thing somehow...



# %% labeling of selected events: things that are definitely NOT fast-events
# %% seeing that APs and spikeshoulderpeaks got detected and labeled correctly
# plotting this in parts: make sure to close plots in between or memory may run out
singleneuron_data.plot_rawdatablocks('gapFree', events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
# %%
singleneuron_data.plot_rawdatablocks('light', events_to_mark=(aps | spikeshoulderpeaks), time_axis_unit='s')
# %%
lightevoked_aps = aps & des_df.applied_ttlpulse
spontaneous_aps = aps & ~des_df.applied_ttlpulse
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

# removing AP label from large-amp light-evoked responses without shoulder:
# non_ap_evokedevents = lightevoked_aps&(des_df.baselinev<-43)
# singleneuron_data.depolarizing_events.loc[non_ap_evokedevents,'event_label'] = None
# singleneuron_data.write_results()

# %% quick check: all events that do not (yet) have labels are subthreshold depolarizing events
singleneuron_data.plot_rawdatablocks('gapFree', events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))
# %%
singleneuron_data.plot_rawdatablocks('light', events_to_mark=~(currentpulsechanges | aps | spikeshoulderpeaks))

# %% labeling noise-events
# there are rather many 'events' in the stretches of recording where this neuron is behaving rather noisily,
# but they occur at depolarized baselinev and tend to be rather small (naked eye says fast-events are 2mV amp
# and up, while noise-events are ~1mV)
noiseevents_candidates = (des_df.baselinev > -30)  & (des_df.amplitude < 1.8)  # picked the amp.criterion based on seeing events that rise above the noise
spont_noiseevents = noiseevents_candidates & ~des_df.applied_ttlpulse
evoked_noiseevents = noiseevents_candidates & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
                                                      cmeasure='baselinev',
                                                      spont_noisydepols=spont_noiseevents,
                                                      evoked_noisydepols=evoked_noiseevents)
singleneuron_data.plot_depolevents(noiseevents_candidates,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# it doesn't look like I would want to analyze anything about any of these events, except maybe the
# single one that was evoked... So labeling the spont ones as noiseevents:
# singleneuron_data.depolarizing_events.loc[spont_noiseevents,'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# des_df = singleneuron_data.depolarizing_events

# based on amp vs half-width scatter of unlabeled events, let's also see all small but wide events and decide if they're noise, too:
noiseevents_candidates = (des_df.width_50 > 15)
spont_noiseevents = noiseevents_candidates & ~des_df.applied_ttlpulse
evoked_noiseevents = noiseevents_candidates & des_df.applied_ttlpulse
singleneuron_data.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
                                                      cmeasure='baselinev',
                                                      spont_noisydepols=spont_noiseevents,
                                                      evoked_noisydepols=evoked_noiseevents)
singleneuron_data.plot_depolevents(noiseevents_candidates,
                                   do_baselining=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# in the evoked, events with this half-width are real (>3mV amp, steeply rising responses to light);
# in the spont, these events just look like noise. Labeling them accordingly:
# singleneuron_data.depolarizing_events.loc[spont_noiseevents,'event_label'] = 'noiseevent'
# singleneuron_data.write_results()
# des_df = singleneuron_data.depolarizing_events

# for spont. events, both rise-time and half-width measures seem to have a little gap at amp=1.75mV;
# probably no event <1.75mV amp is a fast-event candidate.
small_spont_unlabeled_events = spont_unlabeled_events & (des_df.amplitude < 1.75)
singleneuron_data.plot_depolevents(small_spont_unlabeled_events,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# indeed, things in there that look like real events all have spikelet-shape. Labeling them
# as 'spikeletcandidate's for now:
# singleneuron_data.depolarizing_events.loc[small_spont_unlabeled_events,'event_label'] = 'spikeletcandidate'
# singleneuron_data.write_results()
# des_df = singleneuron_data.depolarizing_events




# %% labeling of selected events: things that could be fast-events
# first, let's see if some of those largest spont.events look like they could be fast-events
large_spont_events = spont_unlabeled_events & (des_df.amplitude > 15)
singleneuron_data.plot_depolevents(large_spont_events,
                                   do_baselining=True,
                                   do_normalizing=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# events with 15 < amp < 18 mV look like they are probably stacked fast-events (two arriving in quick succession):
# even though rise isn't exactly the same, normalized decays are almost identical.
# The bigger amp ones are definitely something else altogether, and should be easily separable by half-width
plt.figure()
des_df.loc[large_spont_events,'width_50'].plot.hist(bins=20)  # events with half-width > 4ms are of the other kind
# %%
# also from amplitude/half-width scatter it looks like 4ms could be a good cutoff, let's see if this holds
# across all event amplitudes... starting from spont. events, then looking at evoked ones next
spont_narrow_events = spont_unlabeled_events & (des_df.width_50 <= 4)
singleneuron_data.plot_depolevents(spont_narrow_events,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
spont_wide_events = spont_unlabeled_events & (des_df.width_50 > 4)
singleneuron_data.plot_depolevents(spont_wide_events,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
# in the spont. wide events, only the smallest ones (amp up to 3mV) look like they're really just noise,
# all the others are definitely events of some sort.
# in the spont. narrow events, there seems to be one spikeshoulderpeak and a few small-amp things with slow rise.
# %% let's see if a scatter of rise-time vs width shows some grouping:
singleneuron_data.scatter_depolarizingevents_measures('rise_time_10_90', 'width_50', 'baselinev',
                                                      spont_events=spont_unlabeled_events)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_50', 'baselinev',
                                                      spont_events=spont_unlabeled_events)
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'width_30', 'baselinev',
                                                      spont_events=spont_unlabeled_events)


# %%
evoked_narrow_events = evoked_unlabeled_events & (des_df.width_50 <= 4)
singleneuron_data.plot_depolevents(evoked_narrow_events,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )
evoked_wide_events = evoked_unlabeled_events & (des_df.width_50 > 4)
singleneuron_data.plot_depolevents(evoked_wide_events,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   colorby_measure='baselinev',
                                   prealignpoint_window_inms=5,
                                   plotwindow_inms=30,
                                   )


# %%











# %% labeling fast-events as such, and saving the data table
# singleneuron_data.depolarizing_events.event_label[fastevents_candidates] = 'fastevent'
# singleneuron_data.write_results()
# tinyfastevents_largerthan_params = {
#                                 'amplitude':0.4,
#                                 # 'baselinev':-80,
#                                 }
# tinyfastevents_smallerthan_params = {
#                                  'rise_time_20_80': 0.2,
#                                  }
