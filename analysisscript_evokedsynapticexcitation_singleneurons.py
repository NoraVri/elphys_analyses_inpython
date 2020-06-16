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

cell20190527Arawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time',
                                                         cmeasure='baselinev',
                                                         spontevents=cell20190527Aspont_events,
                                                         evokedevents=cell20190527Aevoked_events)
# histogram of baselinev's
cell20190527Arawdata.depolarizing_events.hist('baselinev',bins=80)
# events with baselinev > -25mV are in fact spike-shoulder peaks:
spikeshoulderpeaks = cell20190527Arawdata.depolarizing_events.baselinev > -25
cell20190527Arawdata.plot_depolevents_overlayed(spikeshoulderpeaks,
                                                colorby_measure='baselinev',
                                                prealignpoint_window_inms=20)
# updating events-tables accordingly.
cell20190527Aevoked_events = cell20190527Aevoked_events \
                             & (~spikeshoulderpeaks)
cell20190527Aspont_events = cell20190527Aspont_events \
                            & (~spikeshoulderpeaks)
# %% trying to find further criteria for fast-events:
# although it is clear from the amp/rise-time scatter that there are fast-events,
# it shows no clear boundary between these and spikelets. In fact, there seems to be
# another kind of relatively fast and large event (rise-time up to 1.5ms, amp up to ~3mV).
probablyfastevents = (cell20190527Arawdata.depolarizing_events.amplitude > 2) \
                     & (cell20190527Arawdata.depolarizing_events.rise_time < 1)
cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events&probablyfastevents),
                                                colorby_measure='rise_time',
                                                do_baselining=True,
                                                do_normalizing=True,
                                                prealignpoint_window_inms=5,
                                                total_plotwindow_inms=20)

probablynotfastevents = (cell20190527Arawdata.depolarizing_events.amplitude > 2) \
                     & (cell20190527Arawdata.depolarizing_events.rise_time > 1.2)
cell20190527Arawdata.plot_depolevents_overlayed((cell20190527Aspont_events&probablynotfastevents),
                                                colorby_measure='half_width',
                                                do_baselining=True,
                                                # do_normalizing=True,
                                                prealignpoint_window_inms=5,
                                                total_plotwindow_inms=20)

cell20190527Arawdata.scatter_depolarizingevents_measures('amplitude', 'rise_time',
                                                         cmeasure='half_width',
                                                         prob_fes=probablyfastevents)