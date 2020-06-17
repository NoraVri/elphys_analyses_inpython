# %% putative axonal spine responses in IO neurons.
# focus of this investigation: fast, depolarizing events of highly consistent waveform (as reflected by near-identical
# rise-time and half-width), that fall into groups of different specific amplitudes.

# Q1: can (a) group(s) of such fast-events be identified in the neuron's ongoing spontaneously occurring activity?
# if yes: what are the rise_time / half_width / amplitude parameters that define these events in this neuron?

# Q2: are fast-events included in the neuron's response to synaptic inputs?
# if yes: how reliably are they evoked? Does it depend on light intensity?

# Q3: what is the effect of baselinev on the appearance of fast-events?
# if they indeed represent APs triggered by synaptic inputs in axonal spines, then
# - reducing baselinev should increase the occurrence of large-amplitude fast-events (since they no longer trigger APs)
# - increasing baselinev should increase the overall frequency of fast-events and fast-event-triggered APs

# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
# %% depolarizing events analyses - cell20190527A
cell20190527Arawdata = SingleNeuron('20190527A')
cell20190527Aevoked_events = cell20190527Arawdata.depolarizing_events.applied_ttlpulse
cell20190527Aspont_events = ~cell20190527Arawdata.depolarizing_events.applied_ttlpulse
# %% scatter plot: amplitude vs rise-time
cell20190527Arawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time_20_80',
                                                         cmeasure='half_width',
                                                         spontevents=cell20190527Aspont_events,
                                                         evokedevents=cell20190527Aevoked_events)
# plt.suptitle('all detected events')

# %% scatter plot: half-width vs rise-time
cell20190527Arawdata.scatter_depolarizingevents_measures('half_width', 'rise_time_20_80',
                                                         cmeasure='amplitude',
                                                         spontevents=cell20190527Aspont_events)
cell20190527Arawdata.scatter_depolarizingevents_measures('half_width', 'rise_time_20_80',
                                                         cmeasure='amplitude',
                                                         evokedevents=cell20190527Aevoked_events)
# %% excluding groups of events that definitely do not meet criteria
# events with baselinev > -25mV are in fact spike-shoulder peaks:
spikeshoulderpeaks = cell20190527Arawdata.depolarizing_events.baselinev > -25
# cell20190527Arawdata.plot_depolevents_overlayed(spikeshoulderpeaks,
#                                                 colorby_measure='baselinev',
#                                                 prealignpoint_window_inms=20)
# updating events-tables accordingly:
cell20190527Aevoked_events = cell20190527Aevoked_events \
                             & (~spikeshoulderpeaks)
cell20190527Aspont_events = cell20190527Aspont_events \
                            & (~spikeshoulderpeaks)

# both in spont. and evoked events there is one single one with a much larger amplitude than all the others
# the evoked one looks like it could be real, though it's coming from baselinev ~-30;
# the spont. one looks like a weird noise
verylargeampevents = (cell20190527Arawdata.depolarizing_events.amplitude > 15) & (~spikeshoulderpeaks)
# cell20190527Arawdata.plot_depoleventsgroups_overlayed((verylargeampevents&cell20190527Aspont_events),
#                                                       (verylargeampevents&cell20190527Aevoked_events),
#                                                       group_labels=['spont', 'evoked'],
#                                                       plt_title='strangely large-amp events')
# updating events-tables accordingly:
cell20190527Aspont_events = cell20190527Aspont_events \
                            & (~verylargeampevents)

# 2mV is the smallest amplitude at which a somewhat clear grouping of fast rise_time (20_80 < 0.6 ms) events
# can be seen in the rise-time/amplitude scatter of spontaneous events
# TODO: revisit this criterion to see if there are more fast-events to be fished out of the small depolarizations
# updating events-tables accordingly:
amptoosmall = cell20190527Arawdata.depolarizing_events.amplitude < 2
cell20190527Aevoked_events = cell20190527Aevoked_events \
                             & (~amptoosmall)
cell20190527Aspont_events = cell20190527Aspont_events \
                            & (~amptoosmall)

# the string of spontaneous events in different amplitude-groups all seems to have rise_time_20_80 < 1ms
# in the evoked responses, there may be some that are a spikelet+fast-event;
# in the spontaneous responses there are some intriguing large-amplitude (>5mV) ones that definitely aren't fast-events
# TODO: revisit this criterion to include evoked responses that are fast-event + something
risetimetoolong = cell20190527Arawdata.depolarizing_events.rise_time_20_80 > 1
# cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events & risetimetoolong),
#                                                 colorby_measure='baselinev',
#                                                 do_baselining=True,
#                                                 # do_normalizing=True,
#                                                 total_plotwindow_inms=15
#                                                 )
# plt.suptitle('>1ms rise-time_20_80 events, spontaneous only')
# cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aevoked_events & risetimetoolong),
#                                                 colorby_measure='baselinev',
#                                                 do_baselining=True,
#                                                 # do_normalizing=True,
#                                                 total_plotwindow_inms=15
#                                                 )
# plt.suptitle('>1ms rise-time_20_80 events, evoked only')
# updating events-tables accordingly:
cell20190527Aevoked_events = cell20190527Aevoked_events \
                             & (~risetimetoolong)
cell20190527Aspont_events = cell20190527Aspont_events \
                            & (~risetimetoolong)

# %%










# %%
# first, let's see the large-amplitude events and yet do not have very fast rise-time:
largeampevents = (cell20190527Arawdata.depolarizing_events.amplitude > 10) \
                 & (cell20190527Arawdata.depolarizing_events.amplitude < 15)
cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events&largeampevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=10,
                                                total_plotwindow_inms=50
                                                )
plt.suptitle('large amplitude events')
# the largest one of those looks like a weird noise, updating events-table accordingly
cell20190527Aspont_events = cell20190527Aspont_events & (cell20190527Arawdata.depolarizing_events.amplitude < 15)
# the others look like compound fast-events where the first one has an amplitude of ~5mV and
# doesn't decay until another event is triggered.
#
# let's see if this is also the case for other relatively large-amp but slow rise events:
bigbutslowevents = (cell20190527Arawdata.depolarizing_events.amplitude > 2) \
                   & (cell20190527Arawdata.depolarizing_events.rise_time_20_80 > 1.5) \
                   & (cell20190527Arawdata.depolarizing_events.baselinev < -45)
cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events&bigbutslowevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=10,
                                                total_plotwindow_inms=30
                                                )
plt.suptitle('big yet relatively slow events')
# yea pretty much looks like exactly that, every one of these events looks compound, though it doesn't seem like
# each of these necessarily has a fast-event in there...
# %% now let's see things that really should be fast-events
probablyfastevents = (cell20190527Arawdata.depolarizing_events.amplitude > 3) \
                     & (cell20190527Arawdata.depolarizing_events.rise_time_20_80 < 1.5) \
                     & (cell20190527Arawdata.depolarizing_events.baselinev < -50)  # just to see fewer lines
cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events&probablyfastevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=5,
                                                total_plotwindow_inms=15,
                                                timealignto_measure='rt_midpoint_idx'
                                                )
plt.suptitle('should-be fast-events')
# at the intersection of rise_time_20_80 = ~1ms and amplitude =~5-6mV there seems to be a group of events that is
# too large to be a spikelet but just a bit too slow to be a fast-event, and from the line plot it looks like
# this event also comes in amplitude =~2mV.
# %% narrowing it down to things that are definitely fast-events
definitelyfastevents = (cell20190527Arawdata.depolarizing_events.amplitude > 4) \
                       & (cell20190527Arawdata.depolarizing_events.rise_time_20_80 <= 0.7) \
                       & (cell20190527Arawdata.depolarizing_events.half_width < 4)
cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aevoked_events&definitelyfastevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=5,
                                                total_plotwindow_inms=15,
                                                timealignto_measure='rt_midpoint_idx'
                                                )
plt.suptitle('fast-events only')
# %% find amplitude, rise-time and half-width criteria for each neuron
# - since fast-events have the same shape when normalized, they should also all have the same half-width
# frequency dependence on membrane potential
# evoked groups dependence on membrane potential (when low, we'll see big events that at high vrest become spikes)
cell20190527Arawdata.scatter_depolarizingevents_measures('amplitude', 'half_width',
                                                         cmeasure='rise_time_20_80',
                                                         spontevents=(cell20190527Aevoked_events&definitelyfastevents))

# doublets: possibly one of the axonal spines is capable of activating the AIS
# should always see the same two amplitude events stacked together.