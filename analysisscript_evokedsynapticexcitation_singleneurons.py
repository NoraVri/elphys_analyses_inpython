# %% subthreshold depolarizations and action potentials
# Q1: do they occur spontaneously?
# if yes, with what frequency?

# Q2: are they among the light-evoked responses of the neuron?
# if yes, with what frequency do they occur?

# Q3: what portion of APs is evoked from a fast-event? (both for spontaneous and evoked events)

# Q4: (how) do the answers to Q1-3 depend on the baseline voltage?
# a] do spontaneous APs and fast-events occur more frequently with more depolarized V?
# b] are they evoked more often with more depolarized V?
# c] if we count fast-events + APs evoked from fast-events, is their overall frequency together
#       the same regardless of baseline voltage?
# d] are fast-events more likely to evoke an AP at more depolarized Vrest?

# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
# %% depolarizing events analyses - cell20190527A
cell20190527Arawdata = SingleNeuron('20190527A')
# %% subthreshold depolarizations
# scatter of amp. vs rise-time to see whether there are (groups of)
# depolarizing events that satisfy fast-events criteria;
# separate plots for light-evoked and spontaneous events
cell20190527Aevoked_events = cell20190527Arawdata.depolarizing_events.applied_ttlpulse
cell20190527Aspont_events = ~cell20190527Arawdata.depolarizing_events.applied_ttlpulse

# cell20190527Arawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time',
#                                                          cmeasure='baselinev',
#                                                          spontevents=cell20190527Aspont_events,
#                                                          evokedevents=cell20190527Aevoked_events)
# plt.suptitle('all detected events')

# histogram of baselinev's
# cell20190527Arawdata.depolarizing_events.hist('baselinev',bins=80)

# events with baselinev > -25mV are in fact spike-shoulder peaks:
spikeshoulderpeaks = cell20190527Arawdata.depolarizing_events.baselinev > -25
# cell20190527Arawdata.plot_depolevents_overlayed(spikeshoulderpeaks,
#                                                 colorby_measure='baselinev',
#                                                 prealignpoint_window_inms=20)
# updating events-tables accordingly.
cell20190527Aevoked_events = cell20190527Aevoked_events \
                             & (~spikeshoulderpeaks)
cell20190527Aspont_events = cell20190527Aspont_events \
                            & (~spikeshoulderpeaks)
# %% trying to find further criteria for fast-events:
cell20190527Arawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time',
                                                         cmeasure='baselinev',
                                                         spontevents=cell20190527Aspont_events,
                                                         evokedevents=cell20190527Aevoked_events)
plt.suptitle('all detected subthreshold events')
# although it is clear from the amp/rise-time scatter that there are fast-events,
# it shows no clear boundary between these and spikelets. In fact, there seems to be also
# other kinds of relatively fast and large events.
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
                   & (cell20190527Arawdata.depolarizing_events.rise_time_20_80 > 1.5)
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
probablyfastevents = (cell20190527Arawdata.depolarizing_events.amplitude > 2) \
                     & (cell20190527Arawdata.depolarizing_events.rise_time_20_80 < 1.5) \
                     & (cell20190527Arawdata.depolarizing_events.baselinev < -45)  # just to see fewer lines
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
definitelyfastevents = (cell20190527Arawdata.depolarizing_events.amplitude > 2) \
                     & (cell20190527Arawdata.depolarizing_events.rise_time_20_80 <= 0.6)
cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events&definitelyfastevents),
                                                colorby_measure='baselinev',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=5,
                                                total_plotwindow_inms=15,
                                                timealignto_measure='rt_midpoint_idx'
                                                )
plt.suptitle('fast-events only')
