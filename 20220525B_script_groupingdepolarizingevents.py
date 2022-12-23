# %% imports
from singleneuron_class import SingleNeuron
import matplotlib.pyplot as plt
import quantities as pq
import pandas as pd
import numpy as np

neuron_name = '20220525B'
singleneuron_data = SingleNeuron(neuron_name)

# singleneuron_data.plot_rawdatablocks(time_axis_unit='s', segments_overlayed=False)

# notes summary:
#1hr20min recording where it seems that sodium currents become pretty much blocked; however,
# when depolarized cell continues to do fast active things (looks like dendritic calcium spikes).
# seems fastevents (though slowed down for a while) may be persisting, even if full Na-APs are no longer possible.

# %% !note: Any code written below is meant just for telling the story of selecting out the fast-events,
#   and cannot simply be uncommented and run to get exactly the saved results (the console has to be re-initialized
#   after each call to write_results, and maybe other things).
# %% extracting depolarizing events
# notes:
# extracting with default parameter settings except min_depolamp=2

# singleneuron_data.get_depolarizingevents_fromrawdata(min_depolamp=2)
# singleneuron_data.write_results()

# %% plots and analyses: labeling actionpotentials
# des_df = singleneuron_data.depolarizing_events
# aps_oncurrentpulsechange = des_df.event_label == 'actionpotential_on_currentpulsechange'
# aps_evokedbylight = ((des_df.event_label == 'actionpotential') & (des_df.applied_ttlpulse))
# aps_spont = (des_df.event_label == 'actionpotential') & (~des_df.applied_ttlpulse)
# # for each category of APs, see that they are indeed that:
# events = aps_oncurrentpulsechange #aps_evokedbylight  #aps_spont
# blocknames = des_df[events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events,
#                                          segments_overlayed=False)
# no aps_evokedbylight for this neuron.
# aps_oncurrentpulsechange: they're definitely not proper IO APs for the most part, and not all things that
# could/should be counted as AP on currentpulse got picked up as such; but definitely all things that got picked up
# as AP on currentpulsechange can be counted as such.
# aps_spont: almost everything that got picked up as such is in fact evoked by DC current, whether directly or
# from rebound potential triggered by release from -DC. Exceptions are one AP sitting on a depolarizing current pulse
# (not triggered directly by DC, it's the second spike on the pulse) and some things occurring spontaneously while the
# neuron is held with +DC for a while in gapFree_0001.
# spontaps = (aps_spont & ((des_df.file_origin == 'longPulses_0000.abf')
#                          | ((des_df.file_origin == 'gapFree_0001.abf')
#                             & (des_df.baselinev_idx > (120 * 20000))
#                             & (des_df.baselinev_idx < (1134 * 20000)))))
# aps_on_currentpulsechange = aps_spont & ~spontaps
# singleneuron_data.depolarizing_events.loc[aps_on_currentpulsechange, 'event_label'] = 'actionpotential_on_currentpulsechange'
# singleneuron_data.depolarizing_events.loc[spontaps, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()
# %% plots and analyses: seeing and labeling subthreshold depolarizing events
des_df = singleneuron_data.depolarizing_events
nbins = 100
# Seeing that light/puff-evoked things all got labeled as such:
# evoked_events = des_df.applied_ttlpulse
# singleneuron_data.plot_rawdatablocks('light', events_to_mark=evoked_events)
# notes:
# no TTL-evoked activity for this neuron.


# Seeing that spontaneous fast-events got picked up:
spont_events = ~des_df.applied_ttlpulse
unlabeled_events = des_df.event_label.isna() # all events that were not automatically given a label
unlabeled_spont_events = (spont_events & unlabeled_events)
# blocknames = des_df[unlabeled_spont_events].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=unlabeled_spont_events,
#                                          segments_overlayed=False)
# notes:
# Yes, it looks like everything that warranted getting picked up as an event indeed got picked up (the handful
# events with amp < 2mV that my eyes picked up all looked like spikelets to me). However, most of these events occur
# on/near and definitely because of currentpulsechanges (degenerate APs/rebound responses).
# Labeling these as 'events_on_currentpulsechange':
# events_on_currentpulsechange = (unlabeled_spont_events
#                                 & ~((des_df.file_origin == 'gapFree_0001.abf') | (des_df.file_origin == 'gapFree_0002.abf')))
# unlabeled_spont_events = (unlabeled_spont_events & ~events_on_currentpulsechange)
# singleneuron_data.depolarizing_events.loc[events_on_currentpulsechange, 'event_label'] = 'events_on_currentpulsechange'
# singleneuron_data.write_results()

# Finding and labeling fast-events (and other types of events encountered along the way):
# plotting all as-yet unlabeled events parameters:
des_df[unlabeled_spont_events].hist(column=['maxdvdt', 'rise_time_20_80', 'width_50', 'amplitude', 'baselinev'],
                                 bins=nbins,
                                 )
plt.suptitle('all as-yet unlabeled events')
singleneuron_data.scatter_depolarizingevents_measures('maxdvdt', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'amplitude',
                                                      cmeasure='baselinev',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
singleneuron_data.scatter_depolarizingevents_measures('rise_time_20_80', 'maxdvdt',
                                                      cmeasure='amplitude',
                                                      unlabeled_spont_events=unlabeled_spont_events,
                                                      )
# Labeling fast-events and other events fitting in categories not labeled automatically (fastevent, compound_event, other_event, noiseevent)
singleneuron_data.plot_depolevents(unlabeled_spont_events,
                                   colorby_measure='baselinev',
                                   plotwindow_inms=15,
                                   do_baselining=True,
                                   # do_normalizing=True,
                                   plot_dvdt=True
                                   )
# %%
# there are two events (the largest and the smallest of the bunch) that occur at way depolarized membrane potential
# (>-25mV) and I'm not at all sure what they are; then there's four events that look like proper fastevents (all
# amp 4 mV) occurring at resting baselineV and another handful events occurring at moderately depolarized membrane
# potential that start to have too slow rise-time to be considered fast - in fact, they rise so slowly that the baseline
# points aren't always too good, which will be mucking with the extracted measurements, too.
# First, let's see those events occurring at baselineV > -25mV:
# events_underinvestigation = (unlabeled_spont_events & (des_df.baselinev > -25))
# blocknames = des_df[events_underinvestigation].file_origin.unique()
# if len(blocknames) > 0:
#     singleneuron_data.plot_rawdatablocks(*blocknames,
#                                          events_to_mark=events_underinvestigation,
#                                          segments_overlayed=False)
# the large-amp one looks like a dendritic Ca-spike that got picked up weird (that's why the baselineV is so high);
# the tiny event seems to me a sizeable spikelet (~2mV) occurring right on top of a particularly strong oscillation.
# Labeling the big one as AP:
# actionpotential = (events_underinvestigation & (des_df.amplitude > 6))
# singleneuron_data.depolarizing_events.loc[actionpotential, 'event_label'] = 'actionpotential'
# singleneuron_data.write_results()

# The next largest event (amp ~8mV) clearly has a double up-stroke; labeling it as compound_event:
# compound_event = (unlabeled_spont_events & (des_df.amplitude > 7))
# singleneuron_data.depolarizing_events.loc[compound_event, 'event_label'] = 'compound_event'
# singleneuron_data.write_results()

# In the now remaining events, a grouping by maxdVdt appears; let's see if that corresponds to different times in the recording:
events_underinvestigation = (unlabeled_spont_events & (des_df.maxdvdt < 0.12))
blocknames = des_df[events_underinvestigation].file_origin.unique()
if len(blocknames) > 0:
    singleneuron_data.plot_rawdatablocks(*blocknames,
                                         events_to_mark=events_underinvestigation,
                                         segments_overlayed=False)
# no it does not... it seems the events in this neuron slow down for a little while, but then get faster again towards
# the end of recordings (in gapFree_0002, >1hr after establishing patch).
# Very unsure which of these events (not) to label as fastevent...
